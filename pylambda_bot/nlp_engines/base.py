from abc import ABCMeta


class BaseNLPEngine(metaclass=ABCMeta):
    def __init__(self) -> None:
        super(BaseNLPEngine, self).__init__()

    @classmethod
    def get_reply(self, input_text: str, prev_text: str = None) -> str:
        """Get reply message.

        Args:
            input_text (str): input message
            prev_text (str, optional): previous message. Defaults to None.

        Returns:
            str: reply message
        """
        raise NotImplementedError
