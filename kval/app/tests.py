from django.test import TestCase, Client


class HealthCheckIntegrationTest(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()
    
    def test_health_check_returns_200(self) -> None:
        response = self.client.get('/api/health/')
        
        self.assertEqual(response.status_code, 200)