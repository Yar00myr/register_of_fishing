import pytest
from django.urls import reverse
from main.models import FishType


class TestLoginPage:
    def test_get_login_page(self, client):
        url = reverse("main:login")
        response = client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_authenticated_user_redirected(self, auth_client):
        url = reverse("main:login")
        response = auth_client.get(url)
        assert response.status_code == 302
        assert reverse("main:homepage") in response["Location"]

    def test_login_success(self, client, user):
        url = reverse("main:login")
        response = client.post(url, {"username": "testuser", "password": "testpass"})
        assert response.status_code == 302
        assert reverse("main:homepage") in response["Location"]

    def test_login_invalid_credentials(self, client, db):
        url = reverse("main:login")
        response = client.post(url, {"username": "wrong", "password": "wrong"})
        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["form"].errors

    def test_login_empty_form(self, client, db):
        url = reverse("main:login")
        response = client.post(url, {})
        assert response.status_code == 200
        assert not response.context["form"].is_valid()


class TestLogoutPage:
    def test_logout_success(self, auth_client):
        url = reverse("main:logout")
        response = auth_client.post(url)
        assert response.status_code == 302
        assert reverse("main:login") in response["Location"]

    def test_logout_get_not_allowed(self, auth_client):
        url = reverse("main:logout")
        response = auth_client.get(url)
        assert response.status_code == 405

    def test_logout_unauthenticated(self, client, db):
        url = reverse("main:logout")
        response = client.post(url)
        assert response.status_code == 302
        assert reverse("main:login") in response["Location"]


class TestNewFishType:
    def test_create_fish_type_success(self, auth_client):
        url = reverse("main:new_fish_type")
        response = auth_client.post(url, {"name": "Perch"})
        assert response.status_code == 302
        assert FishType.objects.filter(name="Perch").exists()

    def test_create_fish_type_success_message(self, auth_client):
        url = reverse("main:new_fish_type")
        response = auth_client.post(url, {"name": "Perch"}, follow=True)
        messages = [str(m) for m in response.context["messages"]]
        assert "Fish type added successfully!" in messages

    def test_create_fish_type_invalid(self, auth_client):
        url = reverse("main:new_fish_type")
        response = auth_client.post(url, {"name": ""}, follow=True)
        messages = [str(m) for m in response.context["messages"]]
        assert "Failed to add fish type. Please check the form." in messages
        assert not FishType.objects.filter(name="").exists()

    def test_create_fish_type_duplicate(self, auth_client, db):
        FishType.objects.create(name="Carp")
        url = reverse("main:new_fish_type")
        response = auth_client.post(url, {"name": "Carp"}, follow=True)
        messages = [str(m) for m in response.context["messages"]]
        assert "Failed to add fish type. Please check the form." in messages
        assert FishType.objects.filter(name="Carp").count() == 1

    def test_create_fish_type_requires_login(self, client, db):
        url = reverse("main:new_fish_type")
        response = client.post(url, {"name": "Perch"})
        assert response.status_code == 302
        assert "login" in response["Location"]
        assert not FishType.objects.filter(name="Perch").exists()

    def test_create_fish_type_get_not_allowed(self, auth_client):
        url = reverse("main:new_fish_type")
        response = auth_client.get(url)
        assert response.status_code == 405
