"""
custom_param.py

Bandwidth's Custom Param BXML verb

@copyright Bandwidth INC
"""
from ..verb import Verb


class CustomParam(Verb):
    def __init__(self, name: str = None, value: str = None):
        """Initialize a <CustomParam> verb

        Args:
            name (str, optional): The name of this parameter, up to 256 characters. Defaults to None.
            value (str, optional): The value of this parameter, up to 2048 characters. Defaults to None.
        """
        self.name = name
        self.value = value

        super().__init__(
            tag="CustomParam",
        )

    @property
    def _attributes(self):
        return {
            "name": self.name,
            "value": self.value,
        }
