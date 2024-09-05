import httpx
import pytest
from unittest.mock import patch
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from testcontainers.mysql import MySqlContainer
from testcontainers.redis import RedisContainer
from src.modules.database import SessionFactory, Base
from src.main import app
from httpx import AsyncClient
import pytest_asyncio
from src.config import secret_settings
from redis.asyncio import ConnectionPool
import redis.asyncio as redis_asyncio

@pytest_asyncio.fixture(scope="function")
async def containers(monkeypatch):
    """Testcontainers를 사용하여 MySQL과 Redis 컨테이너를 설정합니다."""
    mysql = MySqlContainer("mysql:8.0")
    mysql.with_command(["mysqld", "--default-authentication-plugin=mysql_native_password"])

    redis = RedisContainer("redis:latest")

    mysql.start()
    redis.start()

    test_engine = None
    try:
        # MySQL 환경 변수 설정
        monkeypatch.setenv('DB_USERNAME', mysql.username)
        monkeypatch.setenv('DB_PASSWORD', mysql.password)
        monkeypatch.setenv('DB_HOST', mysql.get_container_host_ip())
        monkeypatch.setenv('DB_PORT', str(mysql.get_exposed_port(mysql.port)))
        monkeypatch.setenv('DB_DBNAME', mysql.dbname)

        # Redis 환경 변수 설정
        monkeypatch.setenv('REDIS_HOST', redis.get_container_host_ip())
        monkeypatch.setenv('REDIS_PORT', str(redis.get_exposed_port(6379)))

        print(f"Using DB_USERNAME={mysql.username}")
        print(f"Using DB_PASSWORD={mysql.password}")
        print(f"Using DB_HOST={mysql.get_container_host_ip()}")
        print(f"Using DB_PORT={mysql.get_exposed_port(mysql.port)}")
        print(f"Using DB_DBNAME={mysql.dbname}")
        print(f"Using REDIS_HOST={redis.get_container_host_ip()}")
        print(f"Using REDIS_PORT={redis.get_exposed_port(6379)}")

        # 설정 다시 로드
        secret_settings.redis_host = redis.get_container_host_ip()
        secret_settings.redis_port = redis.get_exposed_port(6379)

        # Redis 연결 재설정
        redis_url = f"redis://{secret_settings.redis_host}:{secret_settings.redis_port}"
        pool = redis_asyncio.ConnectionPool.from_url(redis_url)

        # 새로운 테스트 엔진과 세션 팩토리 생성
        database_url = f"mysql+aiomysql://{mysql.username}:{mysql.password}@{mysql.get_container_host_ip()}:{mysql.get_exposed_port(mysql.port)}/{mysql.dbname}?auth_plugin=mysql_native_password"
        test_engine = create_async_engine(database_url)
        test_session_factory = async_sessionmaker(bind=test_engine, expire_on_commit=False)

        # 테이블 생성
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # SessionFactory와 엔진 패치
        with patch('src.modules.database.SessionFactory', test_session_factory), \
             patch('src.modules.database.engine', test_engine), \
             patch('src.modules.cache.redis_url', redis_url), \
             patch('src.modules.cache.pool', pool):
            yield

    finally:
        if test_engine:
            # 테스트 후 테이블 삭제
            async with test_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

        mysql.stop()
        redis.stop()


@pytest_asyncio.fixture(scope="function")
async def client(containers):
    """테스트용 HTTP 클라이언트를 제공합니다."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_signup_and_login_logout(client: httpx.AsyncClient):
    # 1. 회원가입 테스트
    username = "testuser"
    realname = "Test User"
    password = "testpass123"

    signup_data = {
        "user_name": username,
        "real_name": realname,
        "password": password
    }
    response = await client.post("/auth/signup", json=signup_data)
    response.json()
    assert response.status_code == 200
    signup_result = response.json()
    print(signup_result)
    assert signup_result["user_name"] == username
    assert signup_result["real_name"] == realname
    assert signup_result["role"] == '0'

    # 2. 로그인 테스트
    login_data = {"user_name": username, "password": password}
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    login_result = response.json()
    assert "access_token" in login_result

    # 3. 로그아웃 테스트
    response = await client.post("/auth/logout")
    assert response.status_code == 200
    logout_result = response.json()
    assert logout_result["message"] == "Logged out successfully"
