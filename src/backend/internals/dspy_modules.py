import dspy 


class RephraserSignature(dspy.Signature):
    """
    Based on the given context, try to rephrase the question asked by the Agent and make sure that the wordings and rephrasing is creative keeping in 
    mind that the rephrasing needs to be done carefully not hurting the sentiments and all.  Only provide the rephrased question as the output.
    """
    context = dspy.InputField(desc="the context containing the question asked by the Agent and the answer given by the patient")
    rephrase = dspy.OutputField(desc="the rephrased question")


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
    

class RephraserModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.module = dspy.ChainOfThought(RephraserSignature)

    def forward(self, prev_context):
        answer = self.module(context=prev_context).rephrase
        return answer