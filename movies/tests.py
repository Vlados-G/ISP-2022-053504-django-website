from django.test import TestCase
from .models import Reviews


class TestMoviesViews(TestCase):

    def test_home_user_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_about_site_page(self):
        response = self.client.get('/pages/about')
        self.assertEqual(response.status_code, 200)

    def test_sign_in_page(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_availability_page(self):
        reviews = Reviews.objects.all()

        for review in reviews:
            response = self.client.get(f'review/<int:pk>/{review.pk}/')
            self.assertEqual(response.status_code, 200)
