"""This module provides a high-level interface for interacting with different database clients."""
from importlib import import_module
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import Field
from pydantic.dataclasses import dataclass

from ..dependencies import PaginateParameters

ResourceId = Annotated[UUID, Field(description="The unique identifier of the resource")]
ResourceObj = Annotated[dict[str, Any], Field(description="The resource object")]
Partial = Annotated[bool | None, Field(description="Perform a partial update")]


class Base:
    """Base client class for interacting with a database.

    Provides the basic interface for performing CRUD operations on a database.
    Derived classes should implement the specific methods for each operation.

    Attributes:
        exception (HTTPException): The exception module to be used for raising HTTP exceptions.
        status (status): The status module to be used for HTTP status codes.

    Args:
        path (str): The path to the database.
        table (str): The name of the table in the database.
    """

    exception = HTTPException
    status = status

    def __init__(self, path: str, table: str) -> None:
        """Initialize the Base class.

        Args:
            path (str): The path to the database.
            table (str): The name of the table in the database.
        """

    async def insert_one(self, resource_id: ResourceId, resource_obj: ResourceObj) -> ResourceObj:
        """Inserts a resource object in the database.

        Args:
            resource_id (ResourceId): The ID of the resource to be inserted.
            resource_obj (ResourceObj): The resource object to be inserted.

        Returns:
            ResourceObj: The resource object containing the ID.

        Raises:
            self.exception: If the resource already exists in the database.
        """
        raise NotImplementedError

    async def select_one(self, resource_id: ResourceId) -> ResourceObj:
        """Retrieves a resource from the database based on the given ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be retrieved.

        Returns:
            ResourceObj: The retrieved resource object.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        raise NotImplementedError

    async def update_one(
        self, resource_id: ResourceId, resource_obj: ResourceObj, partial: Partial = None
    ) -> ResourceObj:
        """Updates a resource in the database based on the given ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be updated.
            resource_obj (ResourceObj): The resource object to be updated.
            partial (Partial): Whether to perform a partial update or replace the entire resource object.
                Defaults to None.

        Returns:
            ResourceObj: The resource object containing the ID.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        raise NotImplementedError

    async def delete_one(self, resource_id: ResourceId) -> None:
        """Deletes a resource from the database based on the given resource ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be deleted.

        Returns:
            None

        Raises:
            self.exception: If the resource is not found in the database.
        """
        raise NotImplementedError

    async def select_many(self, paginate_parameters: PaginateParameters) -> list[ResourceObj]:
        """Retrieves multiple resources from the database based on the given pagination parameters.

        Args:
            paginate_parameters (PaginateParameters): The pagination parameters.

        Returns:
            list[ResourceObj]: A list of objects representing the retrieved resources.
        """
        raise NotImplementedError


@dataclass
class DBSpecification:
    """Represents the specification for a database connection.

    Attributes:
        path (str): Path to the database.
            This field specifies the path to the database file or server.
        client (str): One of available database clients.
            This field specifies the database client to be used for the connection.
            The available options are "Default", "Postgres", "Redis", "SQLite", and "TinyDB".
            Defaults to "Default".
    """

    path: Annotated[str, Field(description="Path to the database")]
    client: Annotated[
        Literal["Default", "Postgres", "Redis", "SQLite", "TinyDB"],
        Field(default="Default", description="One of available database clients"),
    ]


class DB:
    """Represents a database client adapter.

    Attributes:
        client (type[Base]): The underlying client used for specific database operations.

    Methods:
        insert_one(self, *args: Any, **kwargs: Any) -> Any:
            Inserts a single record into the database.

        select_one(self, *args: Any, **kwargs: Any) -> Any:
            Retrieves a single record from the database.

        update_one(self, *args: Any, **kwargs: Any) -> Any:
            Updates a single record in the database.

        delete_one(self, *args: Any, **kwargs: Any) -> Any:
            Deletes a single record from the database.

        select_many(self, *args: Any, **kwargs: Any) -> Any:
            Retrieves multiple records from the database.
    """

    client: Base

    def __init__(self, db_spec: DBSpecification, table: str) -> None:
        """Initialize the DB instance.

        Args:
            db_spec (DBSpecification): The specification for the database connection.
            table (str): The name of the table to interact with.
        """
        client_module = import_module(f".{db_spec.client.lower()}", package=__package__)
        client_class: type[Base] = getattr(client_module, f"{db_spec.client}Client")
        self.client = client_class(db_spec.path, table)

    async def insert_one(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> ResourceObj:
        """Insert a single record into the database.

        Args:
            *args: Positional arguments to be passed to the client's insert_one method.
            **kwargs: Keyword arguments to be passed to the client's insert_one method.

        Returns:
            Coroutine: A coroutine representing the asynchronous insertion operation.
        """
        return await self.client.insert_one(*args, **kwargs)

    async def select_one(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> ResourceObj:
        """Select a single record from the database.

        Args:
            *args: Positional arguments to be passed to the client's select_one method.
            **kwargs: Keyword arguments to be passed to the client's select_one method.

        Returns:
            Coroutine: A coroutine representing the asynchronous selection operation.
        """
        return await self.client.select_one(*args, **kwargs)

    async def update_one(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> ResourceObj:
        """Update a single record in the database.

        Args:
            *args: Positional arguments to be passed to the client's update_one method.
            **kwargs: Keyword arguments to be passed to the client's update_one method.

        Returns:
            Coroutine: A coroutine representing the asynchronous update operation.
        """
        return await self.client.update_one(*args, **kwargs)

    async def delete_one(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Delete a single record from the database.

        Args:
            *args: Positional arguments to be passed to the client's delete_one method.
            **kwargs: Keyword arguments to be passed to the client's delete_one method.

        Returns:
            Coroutine: A coroutine representing the asynchronous deletion operation.
        """
        return await self.client.delete_one(*args, **kwargs)

    async def select_many(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> list[ResourceObj]:
        """Select multiple records from the database.

        Args:
            *args: Positional arguments to be passed to the client's select_many method.
            **kwargs: Keyword arguments to be passed to the client's select_many method.

        Returns:
            Coroutine: A coroutine representing the asynchronous selection operation.
        """
        return await self.client.select_many(*args, **kwargs)
