from .exercise import Exercise
import os
import openai
from dotenv import load_dotenv

REASON_EXPLANATION = {
    "stop": "The model reached the end of the prompt.",
    "length": "The model did not output the full answer due to token limits.",
    "content_filter": "The model was blocked by the content filter.",
    "null": "The model's answer is still in progress or incomplete.",
}
load_dotenv()


class GPT(Exercise):
    def __init__(self, type_of_exercise, profile) -> None:
        super().__init__(type_of_exercise, profile)
        self.previous_info = []

    def get_patient_info(self) -> str:
        res = ""
        for key in self.profile:
            res += f"{key}: {self.profile[key]}\n"
        return res

    def get_previous_info(self) -> list:
        previous_info = []
        for info in self.previous_info:
            print(info)
            previous_info.extend([
                {"role": "assistant", "content": info['exercise']},
                {"role": "user", "content": info['request']}
            ])
        return previous_info

    def get_patient_info(self) -> str:
        """Returns the patient info."""

    def gen_exercise(self) -> str:
        """Returns the exercise for the patient."""
        # Load your API key from an environment variable or secret management service
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Prompt
        content = f"""
Generate an exercise for speech therapy, of type {self.type_of_exercise}, for the following patient:

{self.get_patient_info()}

Please stay true to the patient's profile.
        """

        print(content)

        messages = [
            {"role": "system", "content": "A bot that generates engaging exercises for speech therapy patients."}]
        messages.append({"role": "user", "content": content})
        messages.extend(self.get_previous_info())

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return_value = None

        if response.choices:
            answer = response.choices[0]
            message = answer.message.content.strip("\"")
            if len(answer.message.content.strip("\"").split("\n")) > 1:
                message = answer.message.content.strip("\"").split("\n")[-1]

            if answer.finish_reason == "stop":
                return_value = {
                    "exercise": message,
                }
            else:

                return_value = {
                    "exercise": message,
                    "warning": REASON_EXPLANATION[answer.finish_reason]
                }
        else:
            return_value = {
                "error": "There was an error generating the exercise.",
                "response": response
            }

        return return_value
