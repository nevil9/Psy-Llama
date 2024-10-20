from .dspy_modules import *
import json
import requests
import re

# def extract_integer_from_text(text):
#     match = re.search(r'\[\s*(\d+)\s*\]', text)
#     if match:
#         return int(match.group(1))
#     else:
#         return None
    
# import re

def extract_integer_from_text(text):
    match = re.search(r'\d+', text)  # Search for any number in the text
    if match:
        return int(match.group())
    else:
        return None
    
def get_api_response(prompt):
    """
    Sends a GET request to the API endpoint with the given prompt and returns the response.

    Parameters:
    - prompt (str): The prompt to send to the API.

    Returns:
    - response_text (str): The response from the API as text.
    """
    # Define the base URL of the API endpoint
    base_url = f'http://192.168.100.78:8001/make_inference?message={prompt}'

    # Define the parameters for the GET request


    try:
        # Send the GET request to the API endpoint
        response = requests.get(base_url)
        json_str = response._content.decode('utf-8')
        response = json.loads(json_str)

        # Check if the request was successful
        if response["error_message"] == None:
            # Return the response text
            return response["data"]["inference_result"]  # or response.json() if the response is in JSON format
        else:
            # Handle unsuccessful requests
            error_message = response["error_message"]
            print(f"Error: Received status code {error_message}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., network errors)
        print(f"An error occurred: {e}")
        return None
    
# Rephraser Prompt
REPHRASER_PROMPT = """
Instruction: Given a context containing the Agent's question and the patient's answer, and a theme to address, rephrase the Agent's question in a creative and sensitive manner. Ensure the rephrased question does not hurt the patient's sentiments and is free of any profanity (ignore any profanity in the context). Only output the rephrased question.
"""

REPHRASER_PROMPT = """
Task: The patient didn't understand the Agent's previous question. Rephrase the Agent's question in a clear and sensitive manner so the patient can understand it. Only output the rephrased question.
"""

# Mapping Prompt
MAPPING_PROMPT = """
Instruction: Evaluate the patient's answer to a question based on the provided context (which includes the question and the patient's answer). Determine and output one of the following decisions:

- **PASS**: The answer satisfactorily addresses the question's intent; proceed to the next question.
- **SKIP**: The patient wishes to abstain from answering; skip to the next question.
- **RETRY**: The answer does not satisfactorily address the question; the question may need to be reassessed or rephrased.
------
**Expected Output**: Respond with only one word: **PASS**, **SKIP**, or **RETRY**, corresponding to the most appropriate decision based on the context.
--------
    For Example:

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
--------
"""

MAPPING_PROMPT = """
Task: Given a context containing question posed by Agent and User's answer, decide whether to PASS, SKIP, or RETRY the question:
PASS: The answer satisfactorily addresses the question's intent.
SKIP: The patient chooses not to answer explicitly, for eg asking to move on or is uncomfortable answering the question.
RETRY: If and only if the patient is unclear about the question and asks for further clarification. If not then the decision should be eithe SKIP or PASS.
Expected Output: Respond with only one word: PASS, SKIP, or RETRY.
"""

# Asker Prompt
ASKER_PROMPT = """
Instruction: Given a theme related to a mental health concern from the PHQ-9 questionnaire, rephrase the theme into an empathetic and concise question. The question should prompt the patient to reflect on how many days they have been experiencing the issue. Ensure the question is kind, sensitive, non-judgmental, and directly addresses the duration of the problem in terms of days, making the patient feel comfortable to answer. Only output the rephrased question.
"""

# Evaluator Prompt
EVALUATOR_PROMPT = """
Instruction: Based on the patient's description of their problem, assess and map the duration they've been experiencing it to one of the following scales:

- **0**: Not at all
- **1**: Several days
- **2**: More than half the days
- **3**: Nearly every day

**Expected Output**: Provide the text corresponding to the best-fitting number (0, 1, 2, or 3) from the options above. Only output one of the following phrases:

- Not at all
- Several days
- More than half the days
- Nearly every day
"""

EVALUATOR_PROMPT = """
Task: Given a context of Agent's question and the User's response, and a list of options, select the most appropriate option from the provided list
that best matches the User's response. Only generate the selected option which best suits the patient's response to the question posed. Please don't generate
any explanation for the answer. Directly generate the appropriate option, and the OPTIONS MUST CONTAIN THE OPTION NUMBER AND OPTION TEXT FROM THE LIST OF OPTIONS. 
"""


ASKER_OPTIMIZED_PROMPT = """
You are provided with a theme related to a mental health concern from the PHQ-9 questionnaire. Your task is to rephrase this theme into an empathetic and 
concise question that prompts the patient to reflect on how many days they have been experiencing the issue. The question should be kind, sensitive, 
and non-judgmental, ensuring that the patient feels comfortable answering. Make sure the question directly addresses the duration of the problem, in terms of days, 
without hurting the patient's feelings. Only provide the rephrased question as the output.

---

Follow the following format.

Theme: theme described in a simple line
Rephrase: The question addressing to the theme

---

Theme: %s
Rephrase:
"""
MAPPER_OPTIMIZED_PROMPT = """\n\n\nGiven a question and the patient\'s corresponding answer, evaluate the response using the following criteria:\n\nPASS: The answer satisfactorily addresses the question\'s intent, and you can move on.\nSKIP: The patient appears to want to abstain from answering the question; move on to the next one.\nRETRY: The answer does not satisfactorily address the question and may need to be reassessed (e.g., if the patient didn\'t understand the question properly).\nRespond with only one of these three words: PASS, SKIP, or RETRY, corresponding to the scenario that best fits the given context.\n\nExamples:\nContext: "It\'s been some days"\nOutput: RETRY\n\nContext: "I didnt get that"\nOutput: RETRY\n\nContext: "What?"\nOutput: RETRY\n\nContext: "I think I have been having this problem for 3-4 days"\nOutput: PASS\n\nContext: "Come again?"\nOutput: RETRY\n\nContext: "I probably dont wanna answer that."\nOutput: SKIP\n\nContext: "Ive been feeling like this almost every day for the past week."\nOutput: PASS\n\nContext: "Sorry, I dont want to talk about this."\nOutput: SKIP\n\nContext: "I think Ive had this problem on and off, maybe half the time."\nOutput: PASS\n\nContext: "Can you repeat the question?"\nOutput: RETRY\n\nContext: "I dont feel comfortable answering this right now."\nOutput: SKIP\n\nContext: "I have no idea how long it\'s been."\nOutput: RETRY\n\n---\n\nFollow the following format.\n\nContext: the context containing the question asked by the evaluator and the answer given by the patient\nOutputs: PASS, SKIP or RETRY\n\n---\n\nContext: %s\Outputs : """
EVALUATOR_OPTIMIZED_PROMPT = """
Based on the patient's description of their problem, assess how long they've been experiencing it using this scale:

0: Not at all
1: Several days
2: More than half the days
3: Nearly every day

Provide the text corresponding to the ideal number (0, 1, 2, or 3)
Outputs should be among [Not at all, Several Days, More than half the days, Nearly every day]
Just give me the output only.

---

Follow the following format.

Inputs: Patient's answer
Outputs: The best mapping

---

Inputs: %s
Outputs:
"""

REPHRASER_OPTIMIZED_PROMPT = """
Based on the given context and a theme, try to rephrase the question asked by the Agent and make sure that the wordings and rephrasing is creative keeping in 
mind that the rephrasing needs to be done carefully not hurting the sentiments and all.  Only provide the rephrased question as the output. 
Even if there is any profanity just ignore it and rephrase the  question alone and ask the question alone.

---

Follow the following format.

Context: the context containing the question asked by the Agent and the answer given by the patient

Theme: the theme on which the question needs to be addressed

Reasoning: Let's think step by step in order to ${produce the rephrase}. We ...

Rephrase: the rephrased question

---

Context: %s
Theme : %s 
Rephrase : 
"""
class Chatbot_M:

    def __init__(self, km=None):
        # Initialize all modules
        self.asker_module = AskerModule()
        self.mapping_module = MappingModule()
        self.evaluator_module = EvaluatorModule()
        self.rephraser_module = RephraserModule()

        # self.aux_model = auxilliary_model
        # self.kno_model = knowledge_model

        # Initialize conversation and questionnaire state
        self.km = km
        self.messages = []
        self.counter_index = 0
        self.questions = [
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
        self.questionnaire_started = False
        self.questionnaire_finished = False
        self.TRIALS = 7

        self.questions = self.questions[:self.TRIALS]

        # Store answers in a dictionary
        self.answers = {key: {} for key in self.questions}

    def respond(self, user_message):
        """
        Handles the chatbot response based on the user's input.
        """
        if not self.questionnaire_started:
            # Start questionnaire and ask the first question
            self.questionnaire_started = True
            return self._ask_question()

        if self.questionnaire_finished:
            return "Thanks for taking the test."

        # Evaluate the current answer
        self.add_message("User", user_message)
        prev_context = self.get_previous_context()

        # (TODO) Do it in context of self.knowledge_model 
        evaluated_answer = self.evaluator_module(user_message)
        decision = self.mapping_module(prev_context)

        if decision.__contains__("RETRY"):
            # Rephrase and ask the question again
            return self._retry_question(prev_context)
        else:
            # Store the evaluated answer and move to the next question
            self.answers[self.questions[self.counter_index -1]] = evaluated_answer.outputs if decision.__contains__("PASS") else "Didn't wanna answer" # replace this with an intent analyser
            return self._ask_question()

    def _ask_question(self):
        """
        Asks the next question. If all questions are asked, mark the questionnaire as finished.
        """
        if self.counter_index >= len(self.questions):
            self.questionnaire_finished = True
            return "Thanks for taking the test."

        question_theme = self.questions[self.counter_index]

        # (TODO) Do it in context of the auxiliary model
        question_rephrased = self.asker_module(question_theme)
        self.add_message("Agent", question_rephrased)

        # Increment counter to move to the next question in the next round
        self.counter_index += 1
        return question_rephrased

    def _retry_question(self, prev_context):
        """
        Rephrases and retries the current question based on the user's previous answer.
        """
        question_theme = self.questions[self.counter_index - 1]

        # (TODO) Do it in context of the auxiliary model
        rephrased_question = self.rephraser_module(question_theme, prev_context)
        self.add_message("Agent", rephrased_question)
        return rephrased_question

    def get_previous_context(self):
        """
        Get the last two exchanges (agent and user) as the previous context.
        """
        return "\n".join(self.messages[-2:])

    def add_message(self, role, message):
        """
        Adds a message to the conversation history.
        """
        self.messages.append(f"{role}: {message}")


    def get_updated_answers(self):
        """
        Returns the dictionary of answers, filtered to only include updated entries.
        """
        return {k: v for k, v in self.answers.items() if v is not None}
    
    def evaluate_condition(self):
        """
        Placeholder for additional condition evaluations in the future.
        """
        pass


class Chatbot_m:
    def __init__(self, knowledge_model, auxilliary_model, use_optimized_prompt=False):
        self.asker_prompt = ASKER_PROMPT
        self.mapping_prompt = MAPPING_PROMPT
        self.evaluator_prompt = EVALUATOR_PROMPT
        self.rephraser_prompt = REPHRASER_PROMPT
        self.use_optimized_prompt = use_optimized_prompt
        if use_optimized_prompt:
            self.asker_prompt = ASKER_OPTIMIZED_PROMPT
            self.mapping_prompt = MAPPER_OPTIMIZED_PROMPT
            self.evaluator_prompt = EVALUATOR_OPTIMIZED_PROMPT
            self.rephraser_prompt = REPHRASER_OPTIMIZED_PROMPT


        self.km = knowledge_model
        self.nm = auxilliary_model
        self.messages = []
        self.counter_index = 0
        self.questions = [
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
        self.questionnaire_started = False
        self.questionnaire_finished = False
        self.TRIALS = 7

        self.questions = self.questions[:self.TRIALS]
        self.options_list = ["[1] Not at all", "[2] Several Days", "[3] More than half days", "[4] Nearly every day"]
        
        # Store answers in a dictionary
        self.answers = {key: {} for key in self.questions}

    def compute_score(self):
        t = self.answers
        scores = []
        for k, v in t.items():
            if v["score"] != -1:
                scores.append(v["score"]) 

        if len(scores) == 0 : 
            return "Undefined"
        elif sum(scores)/(4*len(scores)) <= 0.25:
            return "Minimal Anxiety"
        elif sum(scores)/(4*len(scores)) <= 0.5:
            return "Mild Anxiety"
        elif sum(scores)/(4*len(scores)) <= 0.75:
            return "Moderate Anxiety"
        else : 
            return "Sever Anxiety"



    def respond(self, user_message):
        """
        Handles the chatbot response based on the user's input.
        """
        if not self.questionnaire_started:
            # Start questionnaire and ask the first question
            self.questionnaire_started = True
            return self._ask_question()

        if self.questionnaire_finished:
            return "Thanks for taking the test."

        # Evaluate the current answer
        self.add_message("User", user_message)
        prev_context = self.get_previous_context()

        options = "\n".join(self.options_list)

        refactored_prompt = self.evaluator_prompt + f" Context : {prev_context} \n Options : {options}" if not self.use_optimized_prompt else self.evaluator_prompt % (user_message)
        # evaluated_answer = self.km(refactored_prompt) # USE KNOWLEDGE MODEL
        evaluated_answer = get_api_response(refactored_prompt)
        score = extract_integer_from_text(evaluated_answer)


            
        # decision = self.mapping_module(prev_context)

        decision_prompt = self.mapping_prompt + f" Context : {prev_context}" if not self.use_optimized_prompt else self.mapping_prompt % (prev_context)
        decision = self.nm(decision_prompt)  # USE NORMAL MODEL
        print(decision)
        if decision.__contains__("RETRY"):
            # Rephrase and ask the question again
            return self._retry_question(prev_context)
        else:
            # Store the evaluated answer and move to the next question
            self.answers[self.questions[self.counter_index -1]] = {"response" : evaluated_answer, "score": score} if decision.__contains__("PASS") else {"resonse":"Didn't wanna answer", "score":-1} # replace this with an intent analyser
            
            return self._ask_question()

    def _ask_question(self):
        """
        Asks the next question. If all questions are asked, mark the questionnaire as finished.
        """
        if self.counter_index >= len(self.questions):
            self.questionnaire_finished = True

            pd = self.compute_score()
            self.answers["Provisional Diagnosis"] = pd

            return "Thanks for taking the test."

        question_theme = self.questions[self.counter_index]

        # (TODO) Do it in context of the auxiliary model
        # question_rephrased = self.asker_module(question_theme)
 
        refactored_prompt = self.asker_prompt + f"\nInput : {question_theme}" if not self.use_optimized_prompt else self.asker_prompt % (question_theme)
        question_rephrased = get_api_response(refactored_prompt) # USE KNOWLEDGE MODEL

        self.add_message("Agent", question_rephrased)

        # Increment counter to move to the next question in the next round
        self.counter_index += 1
        return question_rephrased

    def _retry_question(self, prev_context):
        """
        Rephrases and retries the current question based on the user's previous answer.
        """
        question_theme = self.questions[self.counter_index - 1]

        # (TODO) Do it in context of the auxiliary model
        # rephrased_question = self.rephraser_module(question_theme, prev_context)
        refactored_prompt = self.rephraser_prompt + f" \nInput : Previous Context = {prev_context} & Question Theme = {question_theme}" if not self.use_optimized_prompt else self.rephraser_prompt %  (prev_context, question_theme)
        rephrased_question = self.km(refactored_prompt) # USE KNOWLEDGE MODEL
        self.add_message("Agent", rephrased_question)
        return rephrased_question

    def get_previous_context(self):
        """
        Get the last two exchanges (agent and user) as the previous context.
        """
        return "\n".join(self.messages[-2:])

    def add_message(self, role, message):
        """
        Adds a message to the conversation history.
        """
        self.messages.append(f"{role}: {message}")

    def get_updated_answers(self):
        """
        Returns the dictionary of answers, filtered to only include updated entries.
        """
        return {k: v for k, v in self.answers.items() if v is not None}