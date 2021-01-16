from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def get_user(email, password):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user(self):
        """Creating a new user succeeds."""
        email = 'sample@gmail.com'
        password = 'password'
        user = get_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_no_email(self):
        """Creating a new user without an email fails."""
        with self.assertRaises(ValueError):
            get_user(None, "password")

    def test_create_superuser(self):
        """Createing a superuser succeeds."""
        superuser = get_user_model().objects.create_superuser(
            'admin@gmail.com', 'password'
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_archive(self):
        """Creating an archive succeeds."""
        archive = models.Archive.objects.create(
            user=get_user('sample@gmail.com', 'password'),
            name='Archive1'
        )

        self.assertEqual(str(archive), 'Archive1')

    def test_create_image(self):
        """Creating an image succeeds."""
        archive = models.Archive.objects.create(
            user=get_user('sample@gmail.com', 'password'),
            name='Archive1'
        )
        image = models.Image.objects.create(
            archive=archive,
            name='Image1'
        )

        self.assertEqual(str(image), 'Image1')
