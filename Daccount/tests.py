from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .middleware import SessionIdleTimeoutMiddleware


class SessionIdleTimeoutTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='idle-test')
        self.client.force_login(self.user)
        self.profile_url = reverse('Daccount:profile')

    @patch('Daccount.middleware.time')
    def test_activity_renews_idle_timeout(self, clock):
        timeout = SessionIdleTimeoutMiddleware.idle_timeout
        for timestamp in (100, 100 + timeout - 1, 100 + 2 * (timeout - 1)):
            clock.time.return_value = timestamp
            self.assertEqual(self.client.get(self.profile_url).status_code, 200)

    @patch('Daccount.middleware.time')
    def test_inactive_session_expires_at_three_days(self, clock):
        clock.time.return_value = 100
        self.assertEqual(self.client.get(self.profile_url).status_code, 200)

        clock.time.return_value += 3 * 24 * 60 * 60
        self.assertRedirects(
            self.client.get(self.profile_url),
            f"{reverse('Daccount:login')}?next={self.profile_url}",
            fetch_redirect_response=False,
        )
        self.assertNotIn('_auth_user_id', self.client.session)
