from internals import *
import dspy 

chatbot = Chatbot_M()


while True : 

    user_input = input("User : ").strip()
    agent_output = chatbot.respond(user_input)
    print("Agent : {}".format(agent_output))
