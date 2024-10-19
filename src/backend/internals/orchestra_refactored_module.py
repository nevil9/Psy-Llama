from .dspy_modules import *


class Chatbot_M:

    def __init__(self):
        # Initialize all modules
        self.asker_module = AskerModule()
        self.mapping_module = MappingModule()
        self.evaluator_module = EvaluatorModule()
        self.rephraser_module = RephraserModule()

        # self.aux_model = auxilliary_model
        # self.kno_model = knowledge_model

        # Initialize conversation and questionnaire state
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
