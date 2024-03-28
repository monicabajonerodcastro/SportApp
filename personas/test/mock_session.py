from unittest.mock import MagicMock
from sqlalchemy.orm import Session


class MockSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add = MagicMock()
        self.commit = MagicMock()
        self.rollback = MagicMock()
        self.query = MagicMock()
        self.requests = MagicMock()
