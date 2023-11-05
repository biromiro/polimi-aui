import json


class Exercise:

    def __init__(self, type_of_exercise, profile) -> None:
        self.type_of_exercise = type_of_exercise
        self.profile = profile

    def gen_description(self) -> str:
        """Returns the description of the given name."""
        pass
