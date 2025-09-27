import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.integration.sqlalchemy.models_and_filters import Base, User


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    # Add example users
    session.add_all(
        [
            User(
                first_name="Alice",
                last_name="Smith",
                age=30,
                is_working=True,
                birthday=datetime.date(1993, 4, 20),
                gender="WOMAN",
                created_at=datetime.datetime(2023, 1, 1),
            ),
            User(
                first_name="Bob",
                last_name="Jones",
                age=40,
                is_working=False,
                birthday=datetime.date(1983, 4, 20),
                gender="MAN",
                created_at=datetime.datetime(2022, 5, 1),
            ),
        ]
    )
    session.commit()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
