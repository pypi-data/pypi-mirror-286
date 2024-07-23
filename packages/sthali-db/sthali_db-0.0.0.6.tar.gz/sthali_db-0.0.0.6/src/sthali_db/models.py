"""This module provides classes for creating dynamic models based on field definitions."""
from collections.abc import Callable
from typing import Annotated, Any, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field, create_model  # type: ignore
from pydantic.dataclasses import dataclass


@dataclass
class Default:
    """Represents a default value for an attribute.

    Attributes:
        factory (Callable[[], Any] | None): The function used to create the default value for the attribute.
            Defaults to None.
        value (Any | None): The default value for the attribute. Defaults to None.
    """

    factory: Annotated[
        Callable[..., Any] | None,
        Field(default=None, description="The function used to create the default value for the attribute"),
    ]
    value: Annotated[Any | None, Field(default=None, description="The default value for the attribute")]


@dataclass
class FieldDefinition:
    """Represents a field with its metadata.

    Attributes:
        name (str): Name of the field.
        type (Any): Type annotation of the field.
        default (Default | None): Default value/factory of the field. Defaults to None.
        description (str | None): Description of the field. Defaults to None.
        optional (bool | None): Indicates if the field accepts None. Defaults to None.
        title (str | None): Title of the field. Defaults to None.
    """

    name: Annotated[str, Field(description="Name of the field")]
    type: Annotated[Any, Field(description="Type annotation of the field")]
    default: Annotated[Default | None, Field(default=None, description="Default value/factory of the field")]
    description: Annotated[str | None, Field(default=None, description="Description of the field")]
    optional: Annotated[bool | None, Field(default=None, description="Indicates if the field accepts None")]
    title: Annotated[str | None, Field(default=None, description="Title of the field")]

    @property
    def _metadata(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "description": self.description or f"Field {self.name}",
            "title": self.title or self.name,
        }
        if self.default:
            if self.default.factory:
                result["default_factory"] = self.default.factory
            else:
                result["default"] = self.default.value
        return result

    @property
    def type_annotated(self) -> Annotated[Any, Field]:
        """Returns the type annotation of the field.

        Returns:
            Annotated[Any, Field]: The type annotation of the field.
        """
        field_type = (self.type, self.type | None)[bool(self.optional)]
        return Annotated[field_type, Field(**self._metadata)]


class Base(BaseModel):
    """Represents a base class for models."""


class BaseWithId(Base):
    """Represents a base class for models with a resource identifier."""

    id: Annotated[UUID, Field(description="Resource identifier")]


T = TypeVar("T")


class Models:
    """Represents a collection of models.

    This class is responsible for creating and managing models dynamically based on the provided fields.
    It provides methods to create different types of models such as create, response, and update models.

    Attributes:
        name (str): The name of the collection of models.
        create_model (type[Base]): The dynamically created model for creating new instances.
        response_model (type[BaseWithId]): The dynamically created model for response payloads.
        update_model (type[Base]): The dynamically created model for updating existing instances.
    """

    def __init__(self, name: str, fields: list[FieldDefinition]) -> None:
        """Initialize the Models class.

        Args:
            name (str): The name of the collection of models.
            fields (list[FieldDefinition]): The list of fields definition for the models.
        """
        self.name = name
        self.create_model = self._factory(Base, f"Create{name.title()}", fields)
        self.response_model = self._factory(BaseWithId, f"Response{name.title()}", fields)
        self.update_model = self._factory(Base, f"Update{name.title()}", fields)

    @staticmethod
    def _factory(base: T, name: str, fields: list[FieldDefinition]) -> T:
        fields_constructor = {field.name: field.type_annotated for field in fields}
        return create_model(name, __base__=base, **fields_constructor)  # type: ignore
