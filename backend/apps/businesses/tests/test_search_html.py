import pytest
from django.test import Client

from apps.businesses.models import Business


@pytest.mark.django_db
class TestBusinessSearchHtml:
    def setup_method(self):
        self.client = Client()

    def test_search_endpoint_returns_html(self):
        # Arrange
        biz = Business.objects.create(
            name="Searchable Cafe",
            address="1 Test Street",
            city="Testville",
            postcode="T35 7AA",
            business_type="cafe",
            accessibility_level=3,
        )

        # Act
        resp = self.client.get("/api/v1/search/?search=Searchable")

        # Assert
        assert resp.status_code == 200
        assert "text/html" in resp["Content-Type"]
        # Contains the business name and a link to its fragment
        assert biz.name in resp.content.decode()
        assert f"/api/v1/businesses/{biz.id}/fragment/" in resp.content.decode()

    def test_search_filters_results(self):
        # Arrange two businesses with distinct names
        coffee = Business.objects.create(
            name="Coffee Corner",
            address="2 Bean Road",
            city="Roastown",
            postcode="B33 N11",
            business_type="cafe",
            accessibility_level=4,
        )
        pizza = Business.objects.create(
            name="Pizza Place",
            address="3 Slice Ave",
            city="Cheeseton",
            postcode="P12 ZA1",
            business_type="restaurant",
            accessibility_level=2,
        )

        # Act - search for Coffee only
        resp = self.client.get("/api/v1/search/?search=Coffee")

        # Assert
        body = resp.content.decode()
        assert resp.status_code == 200
        assert "text/html" in resp["Content-Type"]
        assert coffee.name in body
        assert pizza.name not in body
