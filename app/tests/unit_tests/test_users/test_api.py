from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("dudos@dudos.com", "dudos", 200),
    ("dudos@dudos.com", "dudosz", 409),
    ("dudos@vjlink.com", "abshsdasd", 200),
    ("asdadsadas", "dudos", 422)
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("artem@example.com", "artem", 200),
    ("dudos@dudos.com", "asdasdasdasd", 401),
    ("adadasd", "asdasd", 422)
])
async def test_autorization(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code
