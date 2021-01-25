from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Archive
from archive.serializers import ArchiveSerializer


ARCHIVE_LIST_URL = reverse('archive:list')


def archive_detail_url(archive_id):
    """Return URL for showing the detail information of an archive."""
    return reverse('archive:detail', args=[archive_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class ArchiveTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@gmail.com',
            password='password'
        )
        self.client.login(email='test@gmail.com', password='password')

    def test_create_archive(self):
        """Test creating an archive."""
        data = {
            'name': 'test archive',
            'info': 'test info'
        }
        response = self.client.post(ARCHIVE_LIST_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['info'], data['info'])

    def test_get_archive_list(self):
        """Test showing a list of archives."""
        Archive.objects.create(user=self.user, name='archive1')
        Archive.objects.create(user=self.user, name='archive2')

        response = self.client.get(ARCHIVE_LIST_URL)

        archives = Archive.objects.filter(user=self.user).order_by('id')
        serializer = ArchiveSerializer(archives, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_archive(self):
        """Test showing an archive."""
        archive = Archive.objects.create(
            user=self.user,
            name='archive',
            info='서울대학병원 X-Ray 영상 모음'
        )

        response = self.client.get(archive_detail_url(archive.id))

        archive = Archive.objects.get(pk=archive.id)
        serializer = ArchiveSerializer(archive)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_archive(self):
        """Test updating an archive."""
        archive = Archive.objects.create(
            user=self.user,
            name='archive',
            info='서울대학병원 X-Ray 영상 모음'
        )

        data = {
            'name': 'revised archive',
            'info': '강남성모병원 출처 영상'
        }

        response = self.client.put(archive_detail_url(archive.id), data)
        archive.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(archive.name, data['name'])
        self.assertEqual(archive.info, data['info'])

    def test_delete_archive(self):
        """Test deleting an archive."""
        archive = Archive.objects.create(
            user=self.user,
            name='archive',
            info='서울대학병원 X-Ray 영상 모음'
        )

        response = self.client.delete(archive_detail_url(archive.id))
        exists = Archive.objects.filter(name='archive').exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)
