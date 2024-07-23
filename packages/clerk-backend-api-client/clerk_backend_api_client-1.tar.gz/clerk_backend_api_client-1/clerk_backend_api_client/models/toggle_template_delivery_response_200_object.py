from enum import Enum


class ToggleTemplateDeliveryResponse200Object(str, Enum):
    TEMPLATE = "template"

    def __str__(self) -> str:
        return str(self.value)
