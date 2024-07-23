from enum import Enum


class GetTemplateListResponse200ItemObject(str, Enum):
    TEMPLATE = "template"

    def __str__(self) -> str:
        return str(self.value)
