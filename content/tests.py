import io
import os
import tempfile
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from PIL import Image
from unittest.mock import patch, MagicMock

from video.models import Video
from video.api import functions

User = get_user_model()


def get_temp_video_file():
    """
    Create and return a temporary uploaded video file for testing.
    
    Returns:
        SimpleUploadedFile: An in-memory video file with dummy content.
    """
    return SimpleUploadedFile(
        "test_video.mp4",
        b"fake video content",
        content_type="video/mp4"
    )


def get_temp_image():
    """
    Create and return a temporary uploaded image file for testing.
    
    Returns:
        SimpleUploadedFile: An in-memory JPEG image file.
    """
    image = Image.new('RGB', (100, 100))
    tmp_file = io.BytesIO()
    image.save(tmp_file, format='JPEG')
    tmp_file.seek(0)
    return SimpleUploadedFile("thumbnail.jpg", tmp_file.read(), content_type="image/jpeg")


class VideoUploadTest(TestCase):
    """
    TestCase for video upload functionality.
    """
    def setUp(self):
        """
        Setup test environment.
        """
        self.client = APIClient()

    def test_video_upload_success(self):
        """
        Test successful video upload.
        """
        url = reverse('video-upload')
        data = {
            'title': 'Test Upload Video',
            'description': 'Test Description',
            'original_file': get_temp_video_file(),
            'genre': 'action',
        }
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response.data)
        self.assertTrue(Video.objects.filter(title='Test Upload Video').exists())

    def test_video_upload_invalid_data(self):
        """
        Test video upload with invalid data returns 400.
        """
        url = reverse('video-upload')
        data = {
            'title': '',  # Required field empty
            'description': '',
            'original_file': '',
            'genre': ''
        }
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VideoListAPITest(TestCase):
    """
    TestCase for the Video List API endpoint according to specification.
    """
    def setUp(self):
        """
        Setup test environment with authenticated user and test videos.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Erstelle Test-Videos
        self.video1 = Video.objects.create(
            title='Test Movie 1',
            description='Test Description 1',
            original_file=get_temp_video_file(),
            thumbnail=get_temp_image(),
            genre='drama'
        )
        
        self.video2 = Video.objects.create(
            title='Test Movie 2', 
            description='Test Description 2',
            original_file=get_temp_video_file(),
            thumbnail=get_temp_image(),
            genre='comedy'
        )

    def test_video_list_api_structure(self):
        """
        Test that the video list API returns the correct structure according to specification.
        """
        url = reverse('video-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        video_data = response.data[0]
        required_fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']
        
        for field in required_fields:
            self.assertIn(field, video_data)

    def test_video_list_category_mapping(self):
        """
        Test that genre is correctly mapped to category in the API response.
        """
        url = reverse('video-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Finde das Drama-Video in der Response
        drama_video = next(v for v in response.data if v['title'] == 'Test Movie 1')
        self.assertEqual(drama_video['category'], 'Drama')

    def test_video_list_requires_authentication(self):
        """
        Test that the video list endpoint requires authentication.
        """
        self.client.force_authenticate(user=None)
        url = reverse('video-list')
        response = self.client.get(url)
        
        self.assertTrue(response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_video_list_ordering(self):
        """
        Test that videos are ordered by upload_date descending.
        """
        url = reverse('video-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Das zuletzt erstellte Video sollte zuerst kommen
        first_video = response.data[0]
        self.assertEqual(first_video['title'], 'Test Movie 2')


class HLSStreamingTest(TestCase):
    """
    TestCase for HLS streaming endpoints.
    """
    def setUp(self):
        """
        Setup test environment with test video and HLS files.
        """
        self.client = APIClient()
        
        # Erstelle temporäre HLS-Dateien für Tests
        self.temp_dir = tempfile.mkdtemp()
        
        self.video = Video.objects.create(
            title='HLS Test Video',
            description='Test Description',
            original_file=get_temp_video_file(),
            genre='action'
        )

    def test_hls_manifest_endpoint_success(self):
        """
        Test successful HLS manifest retrieval.
        """
        # Mocke das HLS-Manifest
        with patch('video.api.functions.get_hls_manifest_by_resolution') as mock_manifest:
            mock_file = MagicMock()
            mock_file.path = os.path.join(self.temp_dir, 'index.m3u8')
            
            # Erstelle eine Test-M3U8-Datei
            with open(mock_file.path, 'w') as f:
                f.write("#EXTM3U\n#EXT-X-VERSION:3\n")
            
            mock_manifest.return_value = mock_file
            
            url = reverse('hls-manifest', kwargs={'movie_id': self.video.id, 'resolution': '720p'})
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response['Content-Type'], 'application/vnd.apple.mpegurl')
            self.assertEqual(response['Cache-Control'], 'no-cache')

    def test_hls_segment_endpoint_success(self):
        """
        Test successful HLS segment retrieval.
        """
        # Mocke das HLS-Segment
        with patch('video.api.functions.get_hls_segment_path') as mock_segment:
            segment_path = os.path.join(self.temp_dir, '000.ts')
            
            # Erstelle eine Test-TS-Datei
            with open(segment_path, 'wb') as f:
                f.write(b'fake ts content')
            
            mock_segment.return_value = segment_path
            
            url = reverse('hls-segment', kwargs={
                'movie_id': self.video.id, 
                'resolution': '720p', 
                'segment': '000.ts'
            })
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response['Content-Type'], 'video/MP2T')
            self.assertEqual(response['Cache-Control'], 'max-age=31536000')

    def test_hls_manifest_video_not_found(self):
        """
        Test HLS manifest endpoint returns 404 for non-existent video.
        """
        url = reverse('hls-manifest', kwargs={'movie_id': 9999, 'resolution': '720p'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_hls_segment_video_not_found(self):
        """
        Test HLS segment endpoint returns 404 for non-existent video.
        """
        url = reverse('hls-segment', kwargs={
            'movie_id': 9999,
            'resolution': '720p',
            'segment': '000.ts'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_hls_manifest_not_available(self):
        """
        Test HLS manifest endpoint returns 404 when manifest not available.
        """
        with patch('video.api.functions.get_hls_manifest_by_resolution') as mock_manifest:
            mock_manifest.return_value = None
            
            url = reverse('hls-manifest', kwargs={'movie_id': self.video.id, 'resolution': '720p'})
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_hls_segment_not_found(self):
        """
        Test HLS segment endpoint returns 404 for non-existent segment.
        """
        with patch('video.api.functions.get_hls_segment_path') as mock_segment:
            mock_segment.return_value = None
            
            url = reverse('hls-segment', kwargs={
                'movie_id': self.video.id,
                'resolution': '720p',
                'segment': '999.ts'
            })
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VideoFunctionsTest(TestCase):
    """
    TestCase for testing video utility functions.
    """
    def setUp(self):
        """
        Setup test environment with test video.
        """
        self.video = Video.objects.create(
            title='Function Test Video',
            description='Test Description',
            original_file=get_temp_video_file(),
            thumbnail=get_temp_image(),
            genre='comedy'
        )
        self.temp_dir = tempfile.mkdtemp()

    def test_get_hls_manifest_by_resolution(self):
        """
        Test that get_hls_manifest_by_resolution returns correct manifest.
        """
        # Setze HLS-Manifests
        self.video.hls_720p_manifest = 'path/to/720p/index.m3u8'
        self.video.hls_1080p_manifest = 'path/to/1080p/index.m3u8'
        
        result = functions.get_hls_manifest_by_resolution(self.video, '720p')
        self.assertEqual(result, 'path/to/720p/index.m3u8')
        
        result = functions.get_hls_manifest_by_resolution(self.video, '1080p')
        self.assertEqual(result, 'path/to/1080p/index.m3u8')
        
        result = functions.get_hls_manifest_by_resolution(self.video, '480p')
        self.assertIsNone(result)

    def test_get_hls_segment_path_success(self):
        """
        Test successful HLS segment path retrieval.
        """
        # Setup mock manifest
        manifest_path = os.path.join(self.temp_dir, 'index.m3u8')
        segment_path = os.path.join(self.temp_dir, '000.ts')
        
        # Erstelle Test-Dateien
        with open(manifest_path, 'w') as f:
            f.write("#EXTM3U\n")
        with open(segment_path, 'wb') as f:
            f.write(b'test segment')
        
        # Mocke die manifest path
        with patch('video.api.functions.get_hls_manifest_by_resolution') as mock_manifest:
            mock_file = MagicMock()
            mock_file.path = manifest_path
            mock_manifest.return_value = mock_file
            
            result = functions.get_hls_segment_path(self.video, '720p', '000.ts')
            self.assertEqual(result, segment_path)

    def test_get_hls_segment_path_no_manifest(self):
        """
        Test HLS segment path returns None when no manifest exists.
        """
        with patch('video.api.functions.get_hls_manifest_by_resolution') as mock_manifest:
            mock_manifest.return_value = None
            
            result = functions.get_hls_segment_path(self.video, '720p', '000.ts')
            self.assertIsNone(result)

    def test_get_hls_segment_path_segment_not_exists(self):
        """
        Test HLS segment path returns None when segment file doesn't exist.
        """
        manifest_path = os.path.join(self.temp_dir, 'index.m3u8')
        
        # Erstelle nur Manifest, aber kein Segment
        with open(manifest_path, 'w') as f:
            f.write("#EXTM3U\n")
        
        with patch('video.api.functions.get_hls_manifest_by_resolution') as mock_manifest:
            mock_file = MagicMock()
            mock_file.path = manifest_path
            mock_manifest.return_value = mock_file
            
            result = functions.get_hls_segment_path(self.video, '720p', 'nonexistent.ts')
            self.assertIsNone(result)


class VideoModelTest(TestCase):
    """
    TestCase for testing Video model methods and properties.
    """
    def test_video_str_method(self):
        """
        Test the __str__ method of the Video model.
        """
        video = Video(title="Test Video Title")
        self.assertEqual(str(video), "Test Video Title")

    def test_video_category_property(self):
        """
        Test the category property maps genre correctly.
        """
        video = Video(genre="action")
        self.assertEqual(video.category, "Action")
        
        video = Video(genre="sci-fi")
        self.assertEqual(video.category, "Sci-Fi")
        
        video = Video(genre="comedy")
        self.assertEqual(video.category, "Comedy")

    def test_video_creation_with_all_fields(self):
        """
        Test video creation with all required fields.
        """
        video = Video.objects.create(
            title='Complete Test Video',
            description='A complete test video with all fields',
            original_file=get_temp_video_file(),
            thumbnail=get_temp_image(),
            genre='drama'
        )
        
        self.assertEqual(video.title, 'Complete Test Video')
        self.assertEqual(video.genre, 'drama')
        self.assertEqual(video.category, 'Drama')
        self.assertTrue(video.original_file)
        self.assertTrue(video.thumbnail)

    def test_video_hls_fields_optional(self):
        """
        Test that HLS fields are optional and default to None.
        """
        video = Video.objects.create(
            title='Basic Test Video',
            description='Basic video without HLS',
            original_file=get_temp_video_file(),
            genre='action'
        )
        
        self.assertFalse(video.hls_180p_manifest)
        self.assertFalse(video.hls_360p_manifest)
        self.assertFalse(video.hls_720p_manifest)
        self.assertFalse(video.hls_1080p_manifest)