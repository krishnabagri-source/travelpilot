from planner import generate_itinerary, replan_itinerary
import json

from schemas import TripCreate
from database import get_connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import initialize_database


app = FastAPI(title="TravelPilot API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


initialize_database()


@app.get("/")
def root():
    return {
        "message": "TravelPilot backend is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }
@app.post("/api/trips/{trip_id}/generate-itinerary")
def generate_trip_itinerary(trip_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM trips WHERE id = ?",
        (trip_id,)
    )

    trip = cursor.fetchone()

    if trip is None:
        connection.close()

        return {
            "error": "Trip not found"
        }

    trip_data = dict(trip)

    trip_data["interests"] = json.loads(
        trip_data["interests"] or "[]"
    )

    itinerary = generate_itinerary(trip_data)

    connection.close()

    return itinerary
    connection.close()

    return itinerary


@app.post("/api/trips/")
def create_trip(trip: TripCreate):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO trips (
            destination,
            start_date,
            end_date,
            budget,
            currency,
            travelers,
            interests,
            preferences,
            hotel_name,
            hotel_location
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            trip.destination,
            trip.start_date,
            trip.end_date,
            trip.budget,
            trip.currency,
            trip.travelers,
            json.dumps(trip.interests),
            trip.preferences,
            trip.hotel_name,
            trip.hotel_location
        )
    )

    connection.commit()

    trip_id = cursor.lastrowid

    connection.close()

    return {
        "trip_id": trip_id,
        "message": "Trip created successfully"
    }
@app.post("/api/trips/{trip_id}/disruption")
def simulate_disruption(trip_id: int, disruption: dict):

    connection = get_connection()
    cursor = connection.cursor()

    # Find the trip
    cursor.execute(
        "SELECT * FROM trips WHERE id = ?",
        (trip_id,)
    )

    trip = cursor.fetchone()

    if trip is None:
        connection.close()

        return {
            "error": "Trip not found"
        }

    trip_data = dict(trip)

    trip_data["interests"] = json.loads(
        trip_data["interests"] or "[]"
    )

    # Generate the current itinerary
    current_itinerary = generate_itinerary(trip_data)

    # Re-plan the itinerary
    replanned_itinerary = replan_itinerary(
        trip_data,
        current_itinerary,
        disruption
    )

    connection.close()

    return replanned_itinerary



