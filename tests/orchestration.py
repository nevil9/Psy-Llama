import dspy 
import re 

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

class MappingSignature(dspy.Signature):
    """
    Based on a given question and the patient's corresponding answer, evaluate the response according to the following criteria:

    GOOD: The answer satisfactorily addresses the question's intent.
    RETRY: The answer does not satisfactorily address the question and may need to be reassessed. Cases are like if they didn't understand the question properly or something.
    FAIL: The patient appears to want to abstain from answering the question; proceed to the next one. Cases are like they simply refrain from telling you. Give only one word output
    Respond with only one of these three words: GOOD, RETRY, or FAIL, corresponding to the scenario that best fits. 
    """
    context = dspy.InputField(desc="the context containing the question asked by the evaluator and the answer given by the patient")
    outputs = dspy.OutputField(desc="GOOD, RETRY or FAIL")

class AskerSignature(dspy.Signature):
    """
    You are provided with a theme related to a mental health concern from the PHQ-9 questionnaire. Your task is to rephrase this theme into an empathetic and 
    concise question that prompts the patient to reflect on how many days they have been experiencing the issue. The question should be kind, sensitive, 
    and non-judgmental, ensuring that the patient feels comfortable answering. Make sure the question directly addresses the duration of the problem, in terms of days, 
    without hurting the patient's feelings. Only provide the rephrased question.
    """
    theme = dspy.InputField(desc="theme described in a simple line")
    rephrase = dspy.OutputField(desc="The question addressing to the theme")

class EvaluatorSignature(dspy.Signature):
    """
    Based on the patient's description of their problem, assess how long they've been experiencing it using this scale:

    0: Not at all
    1: Several days
    2: More than half the days
    3: Nearly every day

    Provide only the corresponding number (0, 1, 2, or 3).
    """
    inputs = dspy.InputField(desc="Patient's answer")
    outputs = dspy.OutputField(desc="Single number in range 0-3")


class MappingModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.module = dspy.Predict(MappingSignature)

    def forward(self, prev_context):
        decision = self.module(context = prev_context).outputs
        return decision

class AskerModule(dspy.Module):
    def __init__(self):
        super().__init__()

        self.asker_module = dspy.Predict(AskerSignature)

    def forward(self, theme):
        rephrased_question = self.asker_module(theme=theme).rephrase
        return rephrased_question

class EvaluatorModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.module = dspy.Predict(EvaluatorSignature)

    def forward(self, question):
        answer = self.module(inputs=question)
        return answer
    
def get_previous_context(messages):
    prev_context = messages[-2:]
    prev_context_text = "\n".join(prev_context)

    return prev_context_text

def process_question(text):

    match = re.search(r'\*\*Rephrase:\*\* (.+)', text, re.DOTALL)
    if match:
        rephrase = match.group(1).strip()
    else:
        rephrase = text 

    return rephrase

def simulate():

    asker = AskerModule()
    evaluator = EvaluatorModule()
    mapper = MappingModule()

    questions = [
        "Little interest or pleasure in doing things.",
        "Feeling down, depressed, or hopeless.",
        "Trouble falling or staying asleep, or sleeping too much.",
        "Feeling tired or having little energy.",
        "Poor appetite or overeating.",
        "Feeling bad about yourself—or that you are a failure or have let yourself or your family down.",
        "Trouble concentrating on things, such as reading the newspaper or watching television.",
        "Moving or speaking so slowly that other people could have noticed? Or the opposite—being so fidgety or restless that you've been moving around a lot more than usual.",
        "Thoughts that you would be better off dead or of hurting yourself in some way."
    ]

    TRIALS = 4
    questions = questions[:TRIALS]
    index = 0 
    messages = []

    question_theme = questions[index]
    asked_question = asker(question_theme)
    asked_question = process_question(asked_question)
    messages.append("Agent : {}".format(asked_question))

    print("Q: {}".format(asked_question))
    answer = input("A: ").strip()
    messages.append("User : {}".format(answer))

    prev_context = get_previous_context(messages)
    evaluation = evaluator(answer).outputs
    decision = mapper(prev_context)


    condition  = decision

    while index in range(len(questions)) : 
        if condition !="RETRY": 
            index = index + 1
            messages[-1]  = messages[-1] + "\n FINAL VERDICT : {}".format(evaluation)
        
        question_theme = questions[index]
        asked_question = asker(question_theme)
        asked_question = process_question(asked_question)
        messages.append("Agent : {}".format(asked_question))

        print("Q: {}".format(asked_question))
        answer = input("A: ").strip()
        messages.append("User : {}".format(answer))

        prev_context = get_previous_context(messages)
        evaluation = evaluator(answer).outputs
        decision = mapper(prev_context)

        condition  = decision


if __name__ == "__main__":
    simulate()






