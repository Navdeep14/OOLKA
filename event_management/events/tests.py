from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Event, Booking
from django.contrib.auth.models import User

class EventTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.admin = User.objects.create_superuser(username='adminuser', password='password')
        self.event = Event.objects.create(
            name='Test Event',
            date='2023-12-31T23:59:59Z',
            location='Test Location',
            ticket_price=100.00,
            available_tickets=50
        )

    def test_list_events(self):
        url = reverse('event-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_event(self):
        url = reverse('event-list')
        self.client.force_authenticate(user=self.admin)
        data = {
            'name': 'New Event',
            'date': '2023-12-31T23:59:59Z',
            'location': 'New Location',
            'ticket_price': 100.00,
            'available_tickets': 50
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_event(self):
        url = reverse('event-book', args=[self.event.id])
        self.client.force_authenticate(user=self.user)
        data = {
            'tickets': 2,
            'stripe_token': 'tok_visa'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

