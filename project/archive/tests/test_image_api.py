from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Image, Archive
from archive.serializers import ImageSerializer
from cnn_model.model_serving import process_image, predict
from app.settings import CNN_MODEL_PATH
import tempfile
import PIL
import os


def image_list_url(archive_id):
    """Return URL for showing a list of images."""
    return reverse('archive:image-list', args=[archive_id])


def image_detail_url(image_id):
    """Return URL for showing the detail information of an image."""
    return reverse('archive:image-detail', args=[image_id])


def image_upload_url(image_id):
    """Return URL for uploading an image file."""
    return reverse('archive:image-upload', args=[image_id])


def image_predict_url(image_id):
    """Return URL for predicting the probability of pneumonia."""
    return reverse('archive:image-predict', args=[image_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class ImageTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@gmail.com',
            password='password'
        )
        self.client.login(email='test@gmail.com', password='password')
        self.archive = Archive.objects.create(
            user=self.user,
            name='test archive',
            info='archive info'
        )

    def test_create_image(self):
        """Test creating an image."""
        data = {
            'name': 'test image',
            'info': 'image info'
        }
        response = self.client.post(image_list_url(self.archive.id), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['info'], data['info'])

    def test_get_image_list(self):
        """Test showing a list of images."""
        Image.objects.create(archive=self.archive, name='image1')
        Image.objects.create(archive=self.archive, name='image2')

        response = self.client.get(image_list_url(self.archive.id))

        images = Image.objects.filter(archive=self.archive).order_by('id')
        serializer = ImageSerializer(images, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_image(self):
        """Test showing an image."""
        image = Image.objects.create(
            archive=self.archive,
            name='image',
            info='40세 남자, 증상 심한 편'
        )

        response = self.client.get(image_detail_url(image.id))

        image = Image.objects.get(pk=image.id)
        serializer = ImageSerializer(image)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_image(self):
        """Test updating an image."""
        image = Image.objects.create(
            archive=self.archive,
            name='image',
            info='40세 남자, 증상 심한 편'
        )

        data = {
            'name': 'revised image',
            'info': '30세 여자, 가벼운 기침'
        }

        response = self.client.put(image_detail_url(image.id), data)
        image.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(image.name, data['name'])
        self.assertEqual(image.info, data['info'])

    def test_delete_image(self):
        """Test deleting an image."""
        image = Image.objects.create(
            archive=self.archive,
            name='image'
        )

        response = self.client.delete(image_detail_url(image.id))
        exists = Image.objects.filter(name='image').exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)

    def test_upload_image(self):
        """Test uploading an image file."""
        image_instance = Image.objects.create(
            archive=self.archive,
            name='image'
        )
        with tempfile.NamedTemporaryFile(suffix='.jpg') as NTF:
            image = PIL.Image.new('RGB', (50, 50))
            image.save(NTF, format='JPEG')
            NTF.seek(0)
            response = self.client.put(
                image_upload_url(image_instance.id),
                {'image': NTF},
                format='multipart'
            )

            image_instance.refresh_from_db()

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('image', response.data)
            self.assertTrue(os.path.exists(image_instance.image.path))

            image_instance.image.delete()

    def test_predict_image(self):
        """Test predicting the probability of a given image."""
        image_instance = Image.objects.create(
            archive=self.archive,
            name='image'
        )
        with tempfile.NamedTemporaryFile(suffix='.jpg') as NTF:
            image = PIL.Image.new('RGB', (50, 50))
            image.save(NTF, format='JPEG')
            NTF.seek(0)
            self.client.put(
                image_upload_url(image_instance.id),
                {'image': NTF},
                format='multipart'
            )

        response = self.client.put(image_predict_url(image_instance.id))
        image_instance.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('predicted_class', response.data)
        self.assertIn('predicted_value', response.data)
        self.assertTrue(image_instance.predicted_class != None)
        self.assertTrue(image_instance.predicted_value != None)

        image_instance.image.delete()
