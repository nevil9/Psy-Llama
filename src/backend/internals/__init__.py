import dspy 
from .orchestra_module import Chatbot
from .orchestra_refactored_module import Chatbot_M, Chatbot_m


ollama_model = dspy.OllamaLocal(
    model="llama3.1",
    model_type='chat',
    max_tokens=1000,
    temperature=0.1,
    top_p=0.8,
    frequency_penalty=1.17,
    top_k=40
)

dspy.settings.configure(lm=ollama_model)
