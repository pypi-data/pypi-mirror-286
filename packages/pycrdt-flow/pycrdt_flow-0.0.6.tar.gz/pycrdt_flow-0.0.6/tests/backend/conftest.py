import socket
import time

import pytest
import redis
from click.testing import CliRunner
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

import docker
from docker import DockerClient
from pycrdt_flow.backend.app import app as APP
from pycrdt_flow.backend.cli import drop, init


def get_port():
    # Get an unoccupied port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def pg_port(docker_client: DockerClient):
    pg_port = get_port()
    container = None
    try:
        container = docker_client.containers.run(
            "postgres:14",
            detach=True,
            ports={"5432": pg_port},
            remove=True,
            environment={
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "Th3PAssW0rd!1.",
                "POSTGRES_DB": "testdb",
            },
        )
        while True:
            # Execute `pg_isready -U postgres` in the container
            try:
                # Pg is ready
                r = container.exec_run("pg_isready -U postgres")
                assert r.exit_code == 0
                assert b"accepting connections" in r.output
                # Try to connect db
                engine = create_engine(
                    f"postgresql://postgres:Th3PAssW0rd!1.@localhost:{pg_port}/testdb"
                )
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
            except Exception as e:
                time.sleep(0.5)
            else:
                break

        # Empty predefined configs, so we don't bother with initializing dev or prod configs
        runner = CliRunner()
        result = runner.invoke(init, env={"DB_PORT": str(pg_port)})
        assert result.exit_code == 0
        yield pg_port
    finally:
        if container:
            container.stop()


@pytest.fixture(scope="session")
def docker_client():
    try:
        client = docker.from_env()
        client.ping()
        return client
    except:
        pytest.skip("Docker is not available")


@pytest.fixture(scope="session")
def redis_port(docker_client: DockerClient):
    """
    Start a redis container and return the port
    """
    redis_port = get_port()
    container = None
    try:
        container = docker_client.containers.run(
            "redis",
            detach=True,
            ports={"6379": redis_port},
            remove=True,
        )
        time.sleep(1)  # Wait for the server to start
        while True:
            try:
                # Ping redis
                redis_client = redis.Redis(host="localhost", port=redis_port)
                redis_client.ping()
            except:
                time.sleep(0.5)
            else:
                break
        yield redis_port
    finally:
        if container:
            container.stop()


@pytest.fixture
async def app(redis_port, pg_port, monkeypatch):
    monkeypatch.setenv("REDIS_PORT", str(redis_port))
    monkeypatch.setenv("DB_PORT", str(pg_port))

    runner = CliRunner()
    # Drop all before testing
    result = runner.invoke(drop, ["--yes"])
    assert result.exit_code == 0

    # Clear redis data
    redis_client = redis.Redis(host="localhost", port=redis_port)
    redis_client.flushall()

    # Dependencies injection mock
    APP.dependency_overrides = {}
    yield APP


@pytest.fixture
def client(app):
    return TestClient(app)
