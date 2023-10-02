import unittest
from api.v1.views import app_views


class TestAPIRoutes(unittest.TestCase):

    def setUp(self):
        # Set up test client
        self.client = app_views.app.test_client()

    def test_get_status(self):
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'OK'})

    def test_get_stats(self):
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('amenities', response.json)
        # Add more assertions for other keys in the response


if __name__ == '__main__':
    unittest.main()
