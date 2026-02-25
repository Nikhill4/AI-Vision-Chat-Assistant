def get_bot_response(user_message):
    """Generate chatbot response based on user input"""
    if not user_message:
        return "Please enter a message."
    
    message = user_message.lower().strip()

    # Simple rule-based responses
    if "hello" in message or "hi" in message or "hey" in message:
        return "Hello! How can I help you today? You can ask me about AI or upload an image for recognition."
    elif "how are you" in message:
        return "I'm just a bot, but I'm doing great! I'm here to help with image recognition and answer your questions."
    elif "ai" in message or "artificial intelligence" in message:
        return "AI stands for Artificial Intelligence. It's the simulation of human intelligence processes by machines, especially computer systems. This app uses AI for image recognition!"
    elif "image" in message or "recognize" in message or "identify" in message:
        return "You can upload an image and I'll use a neural network (MobileNetV2) to identify what's in it. Try uploading a photo!"
    elif "bye" in message or "goodbye" in message or "quit" in message:
        return "Goodbye! Have a great day! Feel free to return anytime."
    elif "what" in message and "features" in message:
        return "This app has two main features: 1) Image Recognition - Upload images to identify objects, and 2) AI Chat - Ask me questions and I'll help!"
    elif "thank" in message:
        return "You're welcome! Happy to help!"
    elif "?" in message:
        return "That's an interesting question! I'm a simple chatbot, so my responses are limited. Try asking about AI or image recognition, or use the image upload feature."
    else:
        return "I'm a simple chatbot with limited responses. I can help with questions about AI and image recognition. You can also ask me 'hello', 'how are you', 'what features', or upload an image!"
