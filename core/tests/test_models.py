from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def get_user(email, password):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user(self):
        email = 'sample@gmail.com'
        password = 'password'
        user = get_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user(None, "password")

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            'admin@gmail.com', 'password'
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_archive(self):
        archive = models.Archive.objects.create(
            user=get_user('sample@gmail.com', 'password'),
            name='Archive1'
        )

        self.assertEqual(str(archive), 'Archive1')

    def test_create_image(self):
        archive = models.Archive.objects.create(
            user=get_user('sample@gmail.com', 'password'),
            name='Archive1'
        )
        image = models.Image.objects.create(
            archive=archive,
            name='Image1'
        )

        self.assertEqual(str(image), 'Image1')
