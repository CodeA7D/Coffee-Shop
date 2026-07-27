from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class MenuAjaxFeaturesTests(SimpleTestCase):
    def test_menu_filter_ajax_returns_filtered_items(self):
        response = self.client.get("/menu/?ajax=1&category=Cold+Drinks&sort=price")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("Iced Latte", data["items_html"])
        self.assertNotIn("Espresso", data["items_html"])

    def test_search_suggestions_return_matching_products(self):
        response = self.client.get("/menu/search-suggestions/?q=lat")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(len(data["suggestions"]), 1)
        self.assertIn("Vanilla Latte", [item["title"] for item in data["suggestions"]])

    def test_menu_pagination_ajax_returns_next_page_items(self):
        response = self.client.get("/menu/?ajax=1&page=2")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["page"], 2)
        self.assertIn("Brownie Bites", data["items_html"])
        self.assertIn("pagination-link", data["pagination_html"])


class ProfileUpdateTests(TestCase):
    def test_profile_update_persists_new_values_in_session(self):
        response = self.client.post(
            "/profile/update/",
            {"name": "Sara Khan", "email": "sara@example.com"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(self.client.session["profile_name"], "Sara Khan")
        self.assertEqual(self.client.session["profile_email"], "sara@example.com")


class AuthenticationFlowTests(TestCase):
    def test_login_page_uses_email_field(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="email"')

    def test_signup_creates_account_with_email(self):
        response = self.client.post(
            reverse("signup"),
            {
                "email": "newuser@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user_model().objects.filter(email="newuser@example.com").exists())

    def test_password_reset_updates_existing_user_password(self):
        user = get_user_model().objects.create_user(username="resetuser", email="reset@example.com", password="OldPass123!")
        response = self.client.post(
            reverse("password_reset"),
            {
                "email": user.email,
                "new_password1": "NewPass123!",
                "new_password2": "NewPass123!",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.check_password("NewPass123!"))
