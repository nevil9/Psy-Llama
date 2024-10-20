import gradio as gr 

from internals import *
import dspy 
from functools import partial
from langchain_community.llms import Ollama
import requests


llm = Ollama(model="llama3.1")
llm_func = llm.invoke

chatbot = Chatbot_m(knowledge_model=llm_func, auxilliary_model=llm_func)

# chatbot = Chatbot_M()

# Define a function that updates the conversation history and returns it
def chatbot_response(user_input, history):
    # Get the response from the chatbot
    response = chatbot.respond(user_input)
    # Append the user message and chatbot response to the history
    history = history or []
    history.append(("User", user_input))
    history.append(("Agent", response))
    answers = chatbot.get_updated_answers()
    # Get the current index for the progress slider
    current_index = chatbot.counter_index
    return history, history, current_index, answers

# Create a Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("<h1>Chatbot Interface</h1><p>Talk to Chatbot_M!</p>")
    chatbot_ui = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message here...", label="Your Message")
    progress_slider = gr.Slider(minimum=0, maximum=chatbot.TRIALS, step=1, label="Progress", interactive=False)
    answers_output = gr.JSON(label="Updated Answers")
    state = gr.State([])  # For storing the conversation history

    def submit_message(user_input, history):
        history, chat_history, current_index, updated_answers = chatbot_response(user_input, history)
        return history, chat_history, current_index, updated_answers, ""

    msg.submit(submit_message, [msg, state], [chatbot_ui, state, progress_slider, answers_output, msg])

demo.launch(share=True)