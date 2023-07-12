import pytest

from src.main import root, hello

@pytest.mark.asyncio
async def test_root():
    result = await root()
    assert result == {'message': 'Hello World'}


@pytest.mark.asyncio
async def test_name():
    result = await hello("Abhinav")
    assert result == {'message': 'Hello Abhinav'}
