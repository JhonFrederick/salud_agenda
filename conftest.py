import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client(request) -> APIClient:
    client: APIClient = APIClient()
    request.cls.client = client
    return client


@pytest.mark.usefixtures("api_client")
@pytest.mark.django_db
class TestBase:
    @pytest.fixture(autouse=True)
    def _setup(self, request):
        if hasattr(self, "setup"):
            self.setup()
