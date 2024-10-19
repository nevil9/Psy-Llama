import dspy 


class RephraserSignature(dspy.Signature):
    """
    Based on the given context and a theme, try to rephrase the question asked by the Agent and make sure that the wordings and rephrasing is creative keeping in 
    mind that the rephrasing needs to be done carefully not hurting the sentiments and all.  Only provide the rephrased question as the output.
    """
    context = dspy.InputField(desc="the context containing the question asked by the Agent and the answer given by the patient")
    theme = dspy.InputField(desc="the theme on which the question needs to be addressed")
    rephrase = dspy.OutputField(desc="the rephrased question")


class MappingSignature(dspy.Signature):
    """
    Given a question and the patient's corresponding answer, evaluate the response using the following criteria:

    PASS: The answer satisfactorily addresses the question's intent, and you can move on.
    SKIP: The patient appears to want to abstain from answering the question; move on to the next one.
    RETRY: The answer does not satisfactorily address the question and may need to be reassessed (e.g., if the patient didn't understand the question properly).
    Respond with only one of these three words: PASS, SKIP, or RETRY, corresponding to the scenario that best fits the given context.

    Examples:
    Context: "It's been some days"
    Output: RETRY

    Context: "I didnt get that"
    Output: RETRY

    Context: "What?"
    Output: RETRY

    Context: "I think I have been having this problem for 3-4 days"
    Output: PASS

    Context: "Come again?"
    Output: RETRY

    Context: "I probably dont wanna answer that."
    Output: SKIP

    Context: "Ive been feeling like this almost every day for the past week."
    Output: PASS

    Context: "Sorry, I dont want to talk about this."
    Output: SKIP

    Context: "I think Ive had this problem on and off, maybe half the time."
    Output: PASS

    Context: "Can you repeat the question?"
    Output: RETRY

    Context: "I dont feel comfortable answering this right now."
    Output: SKIP

    Context: "I have no idea how long it's been."
    Output: RETRY
    """
    context = dspy.InputField(desc="the context containing the question asked by the evaluator and the answer given by the patient")
    outputs = dspy.OutputField(desc="PASS, SKIP or RETRY")

class AskerSignature(dspy.Signature):
    """
    You are provided with a theme related to a mental health concern from the PHQ-9 questionnaire. Your task is to rephrase this theme into an empathetic and 
    concise question that prompts the patient to reflect on how many days they have been experiencing the issue. The question should be kind, sensitive, 
    and non-judgmental, ensuring that the patient feels comfortable answering. Make sure the question directly addresses the duration of the problem, in terms of days, 
    without hurting the patient's feelings. Only provide the rephrased question as the output.
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

    Provide the text corresponding to the ideal number (0, 1, 2, or 3)
    Outputs should be among [Not at all, Several Days, More than half the days, Nearly every day]
    Just give me the output only.
    """
    inputs = dspy.InputField(desc="Patient's answer")
    outputs = dspy.OutputField(desc="The best mapping")


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
    

class RephraserModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.module = dspy.ChainOfThought(RephraserSignature)

    def forward(self, question_theme ,prev_context):
        answer = self.module(context=prev_context, theme=question_theme).rephrase
        return answer