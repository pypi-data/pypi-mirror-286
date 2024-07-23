from unittest import IsolatedAsyncioTestCase

from sthali_db.dependencies import filter_parameters, PaginateParameters


class TestFilterParameters(IsolatedAsyncioTestCase):
    async def test_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await filter_parameters()


class TestPaginateParameters(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = PaginateParameters()  # type: ignore

        self.assertEqual(result.skip, 0)
        self.assertEqual(result.limit, 100)

    async def test_return_custom(self) -> None:
        result = PaginateParameters(skip=10, limit=10)

        self.assertEqual(result.skip, 10)
        self.assertEqual(result.limit, 10)
