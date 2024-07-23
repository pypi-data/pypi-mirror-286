from unittest import IsolatedAsyncioTestCase
from uuid import uuid4

from sthali_db.models import Any, Base, BaseWithId, Default, FieldDefinition, Models


class TestDefault(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = Default()  # type: ignore

        self.assertEqual(result.factory, None)
        self.assertEqual(result.value, None)

    async def test_return_custom(self) -> None:
        def func() -> None:
            return

        result = Default(factory=func, value=0)

        self.assertEqual(result.factory, func)
        self.assertEqual(result.value, 0)


class TestFieldDefinition(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = FieldDefinition(name="name", type=Any)  # type: ignore

        self.assertEqual(result.name, "name")
        self.assertEqual(result.type, Any)
        self.assertEqual(result.default, None)
        self.assertEqual(result.description, None)
        self.assertEqual(result.optional, None)
        self.assertEqual(result.title, None)

    async def test_return_custom(self) -> None:
        def func() -> None:
            return

        result = FieldDefinition(
            name="name",
            type=str,
            default={"factory": func, "value": 0},  # type: ignore
            description="description",
            optional=True,
            title="title",
        )

        self.assertEqual(result.name, "name")
        self.assertEqual(result.type, str)
        self.assertEqual(result.default.factory, func)  # type: ignore
        self.assertEqual(result.default.value, 0)  # type: ignore
        self.assertEqual(result.description, "description")
        self.assertEqual(result.optional, True)
        self.assertEqual(result.title, "title")

    async def test_type_annotated(self) -> None:
        field_definition = FieldDefinition(name="name", type=str)  # type: ignore

        result = field_definition.type_annotated

        self.assertEqual(result("str"), "str")
        self.assertEqual(result.__args__[0], str)
        self.assertEqual(result.__metadata__[0].title, "name")

    async def test_type_annotated_with_optional(self) -> None:
        field_definition = FieldDefinition(name="name", type=str, optional=True)  # type: ignore

        result = field_definition.type_annotated

        self.assertEqual(result.__args__[0], str | None)

    async def test_type_annotated_with_default_factory(self) -> None:
        def func() -> None:
            return

        field_definition = FieldDefinition(name="name", type=str, default={"factory": func, "value": 0})  # type: ignore

        result = field_definition.type_annotated

        self.assertEqual(result.__metadata__[0].default_factory(), None)

    async def test_type_annotated_with_default_value(self) -> None:
        field_definition = FieldDefinition(name="name", type=str, default={"value": 0})  # type: ignore

        result = field_definition.type_annotated

        self.assertEqual(result.__metadata__[0].default, 0)


class TestBase(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = Base()

        self.assertEqual(result.model_dump(), {})


class TestBaseWithId(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        _id = uuid4()
        result = BaseWithId(id=_id)

        self.assertEqual(result.model_dump(), {"id": _id})


class TestModels(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        _id = uuid4()

        result = Models(name="name", fields=[])

        self.assertEqual(result.name, "name")
        self.assertEqual(result.create_model().model_dump(), {})
        self.assertEqual(result.response_model(**{"id": _id}).model_dump(), {"id": _id})
        self.assertEqual(result.update_model().model_dump(), {})

    async def test_return_custom(self) -> None:
        def func() -> None:
            return

        _id = uuid4()

        result = Models(
            name="name",
            fields=[
                FieldDefinition(name="field1", type=str),  # type: ignore
                FieldDefinition(name="field2", type=str, optional=True),  # type: ignore
                FieldDefinition(name="field3", type=str, default={"factory": func}),  # type: ignore
                FieldDefinition(name="field4", type=str, default={"value": "field4"}),  # type: ignore
                FieldDefinition(name="field5", type=str, default={"factory": func, "value": 1}),  # type: ignore
            ],
        )

        self.assertEqual(result.name, "name")
        self.assertEqual(
            result.create_model(**{"field1": "field1", "field2": None}).model_dump(),
            {"field1": "field1", "field2": None, "field3": None, "field4": "field4", "field5": None},
        )
        self.assertEqual(
            result.response_model(**{"id": _id, "field1": "field1", "field2": None}).model_dump(), # type: ignore
            {"id": _id, "field1": "field1", "field2": None, "field3": None, "field4": "field4", "field5": None},
        )
        self.assertEqual(
            result.update_model(**{"field1": "field1", "field2": None}).model_dump(),
            {"field1": "field1", "field2": None, "field3": None, "field4": "field4", "field5": None},
        )
