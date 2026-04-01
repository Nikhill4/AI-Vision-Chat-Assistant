def _has_image_question(message):
    keywords = ["image", "photo", "picture", "predict", "detected", "recognize", "identify", "confidence", "object"]
    return any(keyword in message for keyword in keywords)


def _format_top_predictions(image_context):
    top_predictions = image_context.get("top_predictions", [])
    if not top_predictions:
        return ""

    formatted = [f"{item['label']} ({item['confidence']:.1f}%)" for item in top_predictions[:3]]
    return ", ".join(formatted)


def get_bot_response(user_message, image_context=None):
    """Generate chatbot response with live context from the latest uploaded image."""
    if not user_message:
        return "Please enter a message."

    message = user_message.lower().strip()
    has_image_context = bool(image_context)

    if any(greet in message for greet in ["hello", "hi", "hey"]):
        if has_image_context:
            top_guess = image_context.get("primary_label", "an object")
            return f"Hello! Based on your latest upload, I currently detect {top_guess}. Ask me for confidence or top predictions."
        return "Hello! Upload an image and I will analyze it, then you can ask detailed questions about what the model sees."

    if not has_image_context and _has_image_question(message):
        return "I don't have an analyzed image yet. Please upload an image first, then I can answer questions about detected objects and confidence."

    if has_image_context:
        primary_label = image_context.get("primary_label", "unknown")
        primary_confidence = image_context.get("primary_confidence", 0.0)
        summary = image_context.get("summary", "No summary available.")
        top_predictions_text = _format_top_predictions(image_context)

        if "top" in message or "alternatives" in message or "other" in message:
            return f"Top model predictions for your latest image: {top_predictions_text}."

        if "confidence" in message or "sure" in message or "accuracy" in message:
            return f"The best class is {primary_label} with {primary_confidence:.1f}% confidence. Other likely classes: {top_predictions_text}."

        if _has_image_question(message) or "what is this" in message or "describe" in message:
            return f"From your latest upload: {summary}. Top predictions: {top_predictions_text}."

        if "features" in message:
            return "You can upload an image for recognition and ask follow-up questions about confidence, top alternatives, and object labels from the model output."

        if "thank" in message:
            return f"You're welcome! If you want, I can explain why {primary_label} was predicted using confidence and alternatives."

        return f"I can help with your latest image prediction. Current result: {summary}. Ask things like 'top predictions' or 'confidence'."

    if "ai" in message or "artificial intelligence" in message:
        return "This assistant uses a MobileNetV2 neural network for image classification and returns confidence-ranked predictions."
    if "how are you" in message:
        return "Ready to analyze images. Upload one and I'll answer context-aware questions about it."
    if "bye" in message or "goodbye" in message or "quit" in message:
        return "Goodbye! Upload another image anytime for a new analysis."
    if "features" in message:
        return "Main features: image recognition with top predictions and context-aware chat based on the most recent uploaded image."
    if "thank" in message:
        return "You're welcome!"

    return "Ask me about the latest uploaded image, or upload one first so I can provide model-based answers."
