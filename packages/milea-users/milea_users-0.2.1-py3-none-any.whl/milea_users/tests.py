from django.contrib.auth import get_user_model
from django.test import TestCase

from milea_notify.models import Setting


class UserCreationTests(TestCase):

    def setUp(self):
        # Erstellen eines Benutzers
        self.user = get_user_model().objects.create_user(email='test@user.com', password='12345')

    def test_user_creation(self):
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_notify_setting_object_created(self):
        self.assertEqual(Setting.objects.count(), 1)
