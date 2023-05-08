from pylambda_bot.nlp_engines.base import BaseNLPEngine


class Echo(BaseNLPEngine):
    def __init__(
        self,
        params: dict = {
            "num_repeat": 1,
        },
        **kwargs,
    ) -> None:
        super().__init__()
        self.params = params

    def get_reply(self, input_text: str, prev_text: str = None):
        """Echo input text.
        Args:
            input_text (str): Prompt text.
        Returns:
            str: Response text.
        """
        return f"{input_text}, " * self.params["num_repeat"]
