import dspy
from openai import OpenAI
from functools import partial

ollama_model = dspy.OllamaLocal(
    model="llama3.1:8b",
    model_type='chat',
    max_tokens=1000,
    temperature=0.1,
    top_p=0.8,
    frequency_penalty=1.17,
    top_k=40
)

bedrock_model = None
knowledge_model = None

# bedrock_model = dspy.Bedrock()
# knowledge_model = dspy.HFClientTGI()

dspy.settings.configure(lm=ollama_model)

openai_api_key = "token-abc123"
openai_api_base = "http://jeu.qblocks.cloud:51243/v1/"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
# completion = client.completions.create(model="meta-llama/Llama-3.2-1B-Instruct",
#                                       prompt="San Francisco is a")
# print("Completion result:", completion)
#
completion_func = partial(client.completions.create, model="meta-llama/Llama-3.2-1B-Instruct")
