# Event Management API

## Overview
This project is a RESTful API service that manages event listings, bookings, and ticket sales.

## Setup and Local Execution

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Set up environment variables for Stripe and database credentials:
    ```
    STRIPE_SECRET_KEY=your_stripe_secret_key
    STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
    ```
5. Run database migrations:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Create a superuser:
    ```
    python manage.py createsuperuser
    ```
7. Start the server:
    ```
    python manage.py runserver
    ```

## API Endpoints

- `GET /api/events`: Lists all available events
- `POST /api/events`: Adds a new event (admin only)
- `GET /api/events/{id}`: Retrieves detailed information about a specific event
- `POST /api/events/{id}/book`: Books tickets for an event

## Third-party API Integrations

- **Google Maps**: Used to display the location of events
- **Stripe**: Used to process ticket payments

## Docker Setup (Bonus)

To run the application in containers, use the provided Dockerfile and docker-compose.yml. Follow these steps:

1. Build the Docker image:
    ```
    docker-compose build
    ```
2. Run the containers:
    ```
    docker-compose up
    ```

## Testing

- Unit tests and integration tests are provided in the `events/tests.py` file. To run the tests, use:
    ```
    python manage.py test
    ```

