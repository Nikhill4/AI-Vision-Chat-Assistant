import { useEffect, useMemo, useState } from "react";
import { checkHealth, predictImage, sendChatMessage } from "./api";

function App() {
  const [healthStatus, setHealthStatus] = useState("checking");

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [prediction, setPrediction] = useState("");
  const [imageContext, setImageContext] = useState(null);
  const [predictError, setPredictError] = useState("");
  const [isPredicting, setIsPredicting] = useState(false);

  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState([
    {
      role: "bot",
      text: "Hello! Ask me about AI, image recognition, or upload an image for prediction."
    }
  ]);
  const [chatError, setChatError] = useState("");
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    let isMounted = true;

    async function loadHealth() {
      try {
        await checkHealth();
        if (isMounted) {
          setHealthStatus("online");
        }
      } catch {
        if (isMounted) {
          setHealthStatus("offline");
        }
      }
    }

    loadHealth();
    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl("");
      return;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);

    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [selectedFile]);

  const statusLabel = useMemo(() => {
    if (healthStatus === "online") return "Backend Online";
    if (healthStatus === "offline") return "Backend Offline";
    return "Checking Backend...";
  }, [healthStatus]);

  async function handlePredict(event) {
    event.preventDefault();
    if (!selectedFile) {
      setPredictError("Please choose an image first.");
      return;
    }

    setIsPredicting(true);
    setPredictError("");
    setPrediction("");
    setImageContext(null);

    try {
      const data = await predictImage(selectedFile);
      setPrediction(data.prediction || "No prediction returned.");
      setImageContext(data.image_context || null);
    } catch (error) {
      setPredictError(error.message);
    } finally {
      setIsPredicting(false);
    }
  }

  async function handleSendMessage(event) {
    event.preventDefault();
    const message = chatInput.trim();
    if (!message) {
      return;
    }

    setChatError("");
    setIsSending(true);
    setChatMessages((current) => [...current, { role: "user", text: message }]);
    setChatInput("");

    try {
      const data = await sendChatMessage(message);
      setChatMessages((current) => [...current, { role: "bot", text: data.reply || "No reply returned." }]);
      if (data.image_context) {
        setImageContext(data.image_context);
      }
    } catch (error) {
      setChatError(error.message);
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>AI Vision Chat Assistant</h1>
        <p>Upload an image for recognition and chat with the assistant in one place.</p>
        <span className={`status-pill ${healthStatus}`}>{statusLabel}</span>
      </header>

      <main className="content-grid">
        <section className="card">
          <h2>Image Recognition</h2>
          <form onSubmit={handlePredict} className="panel-form">
            <label htmlFor="image-input" className="input-label">
              Choose image
            </label>
            <input
              id="image-input"
              type="file"
              accept="image/png,image/jpg,image/jpeg,image/gif,image/bmp"
              onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
            />

            {previewUrl && <img className="preview" src={previewUrl} alt="Selected preview" />}

            <button type="submit" className="primary-btn" disabled={isPredicting}>
              {isPredicting ? "Analyzing..." : "Predict Image"}
            </button>
          </form>

          {prediction && <p className="result">Prediction: {prediction}</p>}
          {predictError && <p className="error">{predictError}</p>}
        </section>

        <section className="card">
          <h2>AI Chat</h2>
          {imageContext && (
            <div className="context-panel">
              <p className="context-title">Latest Image Context</p>
              <p className="context-summary">{imageContext.summary}</p>
              {Array.isArray(imageContext.top_predictions) && imageContext.top_predictions.length > 0 && (
                <ul className="context-list">
                  {imageContext.top_predictions.slice(0, 3).map((item) => (
                    <li key={item.class_id}>
                      {item.label} ({Number(item.confidence).toFixed(1)}%)
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}

          <div className="chat-window">
            {chatMessages.map((message, index) => (
              <div key={`${message.role}-${index}`} className={`chat-bubble ${message.role}`}>
                {message.text}
              </div>
            ))}
          </div>

          <form onSubmit={handleSendMessage} className="chat-form">
            <input
              type="text"
              value={chatInput}
              onChange={(event) => setChatInput(event.target.value)}
              placeholder="Type your message..."
            />
            <button type="submit" className="primary-btn" disabled={isSending}>
              {isSending ? "Sending..." : "Send"}
            </button>
          </form>

          {chatError && <p className="error">{chatError}</p>}
        </section>
      </main>
    </div>
  );
}

export default App;
