from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        event = self.get_object()
        tickets = int(request.data.get('tickets'))
        if tickets > event.available_tickets:
            return Response({'error': 'Not enough tickets available'}, status=status.HTTP_400_BAD_REQUEST)

        total_cost = event.ticket_price * tickets
        try:
            # Process payment
            charge = stripe.Charge.create(
                amount=int(total_cost * 100),  # Stripe works with cents
                currency='usd',
                description=f'Booking for {event.name}',
                source=request.data.get('stripe_token')
            )

            # Update ticket inventory
            event.available_tickets -= tickets
            event.save()

            # Create booking record
            booking = Booking.objects.create(
                user=request.user,
                event=event,
                tickets=tickets,
                total_cost=total_cost
            )

            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

