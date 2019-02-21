from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterTestCase(TestCase):

    # tests valid user; success if redirects to login and creates the user
    def test_registration_view_success(self):
        valid_pass = {
            'username': 'test',
            'password1': 'SecurePass167',
            'password2': 'SecurePass167'
        }
        response = self.client.post(reverse('register'), data=valid_pass)
        self.assertRedirects(response, '/')
        self.assertEqual(User.objects.count(), 1)

    # tests invalid users; success if redirects to registration page and does not create the user
    def test_registration_view_failure(self):
        no_upper = {
            'username': 'test',
            'password1': 'securepass1478963',
            'password2': 'securepass1478963'
        }
        no_lower = {
            'username': 'test',
            'password1': 'SECUREPASS1478963',
            'password2': 'SECUREPASS1478963',
        }
        no_digit = {
            'username': 'test',
            'password1': 'SecurePassword',
            'password2': 'SecurePassword'
        }
        non_matching = {
            'username': 'test',
            'password1': 'SecurePass167',
            'password2': 'SecurePass761'
        }
        non_ascii = {
            'username': 'test',
            'password1': 'SecPass167パスワード',
            'password2': 'SecPass167パスワード'
        }

        response = self.client.post(reverse('register'), data=no_upper)
        self.assertRedirects(response, '/register/')
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(reverse('register'), data=no_lower)
        self.assertRedirects(response, '/register/')
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(reverse('register'), data=no_digit)
        self.assertRedirects(response, '/register/')
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(reverse('register'), data=non_matching)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(reverse('register'), data=non_ascii)
        self.assertRedirects(response, '/register/')
        self.assertEqual(User.objects.count(), 0)
