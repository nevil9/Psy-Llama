from .dspy_modules import *


class Chatbot : 

    def __init__(self):
        self.asker_module = AskerModule()
        self.mapping_module = MappingModule()
        self.evaluator_module = EvaluatorModule()
        self.rephraser_module = RephraserModule()

        self.messages = []
        self.counter_index  = 0 
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

        self.answers = {key:{} for key in range(len(self.questions))}

    def respond(self, user_message):

        if self.questionnaire_started and not self.questionnaire_finished: 

            # Evaluate the user_message and take a decision on to whether continue/move on or retry and accordingly send back new or old question
            self.add_messages("User", user_message)

            # First of all Based on the user_message from the user -> evaluate the answer based on the previous question that was asked 
            prev_context = self.get_previous_context()
            evaluated_answer = self.evaluator_module(user_message)

            # Let the Judge decide what to go ahead with the given answer, evaluation and the question that was asked whether its accurate or not 
            # We need to take a call whehter to move forward or not 

            decision = self.mapping_module(prev_context)

            if decision != "RETRY": 
                # Means we do not have to retry the question --> we move on 
                # In case the counter index has reached the end of questionnaire then no more question module need to be invoked
                self.answers[self.counter_index] = evaluated_answer
                self.counter_index = self.counter_index + 1 

                # Check if self.counter_index has gone beyond the questionnaire --> implies that we have finished all the questions 
                # Ask question only if the questionnaire hasnt been finished
                try : 
                    question_theme = self.questions[self.counter_index]
                    question_rephrased = self.asker_module(question_theme)
                    self.add_messages("Agent", question_rephrased)
                    
                except : 
                    self.questionnaire_finished = True

            elif not self.questionnaire_finished : 
                # If the decision is to RETRY asking the question 
                
                # Need to pass the previous context, answer to a REPHRASER module asking to rephrase it in such a way this time you get the output
                question_theme = self.questions[self.counter_index]
                question_rephrased = self.rephraser_module(question_theme, prev_context)

                self.add_messages("Agent", question_rephrased)  
 
            agentic_output = "Thanks for taking the test ...." if self.questionnaire_finished else question_rephrased

            return agentic_output
        else : 
            self.questionnaire_started = True # Started the questionnaire

            # Ask the question to be asked based on the Question and index that we have 
            question_theme = self.questions[self.counter_index] 
            question_rephrased = self.asker_module(question_theme) # MAKE SURE THAT the question is JUST THE QUESTION

            # We simply return the question as the output
            self.add_messages("Agent", question_rephrased)
            return question_rephrased

        
    
    def get_previous_context(self):
        return "\n".join(self.messages[-2:])
      
  
    def add_messages(self, role, message):
        self.messages.append(f"{role}: {message}")
        

    def evaluate_condition():
        pass
