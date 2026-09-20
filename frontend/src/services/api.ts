const API_BASE_URL = "http://127.0.0.1:8000";

export async function createTrip(tripData: any) {
    const response = await fetch(`${API_BASE_URL}/api/trips/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(tripData),
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(error || "Failed to create trip");
    }

    return await response.json();
}

export async function generateItinerary(tripId: number) {
    const response = await fetch(
        `${API_BASE_URL}/api/trips/${tripId}/generate-itinerary`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        }
    );

    if (!response.ok) {
        const error = await response.text();
        throw new Error(error || "Failed to generate itinerary");
    }

    return await response.json();
}
export async function simulateDisruption(
    tripId: number,
    disruption: any
) {
    const response = await fetch(
        `${API_BASE_URL}/api/trips/${tripId}/disruption`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(disruption),
        }
    );

    if (!response.ok) {
        const error = await response.text();
        throw new Error(
            error || "Failed to simulate disruption"
        );
    }

    return await response.json();
}