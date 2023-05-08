from abc import ABCMeta


class MsgSrvRetryError(Exception):
    """Retry error from message service."""

    pass


class BaseMessageService(metaclass=ABCMeta):
    def __init__(self) -> None:
        super(BaseMessageService, self).__init__()

    @classmethod
    def parse_event(self, event: dict):
        """Parse event data."""
        raise NotImplementedError

    @classmethod
    def gen_res(self, body: str) -> dict:
        """Generate response data.

        Args:
            body (str): body data.

        Returns:
            dict: response data.
        """
        raise NotImplementedError

    @classmethod
    def get_conv_hist(self) -> list:
        """Get previous messages.

        Returns:
            list: List of previous message.
        """
        raise NotImplementedError

    @classmethod
    def post(self, message: str = None) -> None:
        """Post message.

        Args:
            message (str, optional): message to post. Defaults to None.
        """
        raise NotImplementedError
