import { useState } from "react";
import {
    createTrip,
    generateItinerary,
    simulateDisruption,
} from "./services/api";
import "./App.css";

function App() {
    const [form, setForm] = useState({
        destination: "",
        start_date: "",
        end_date: "",
        budget: "",
        currency: "INR",
        travelers: 1,
        interests: "",
        preferences: "",
        hotel_name: "",
        hotel_location: "",
    });

    const [itinerary, setItinerary] = useState(null);
    const [tripId, setTripId] = useState(null);
    const [selectedActivity, setSelectedActivity] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleChange = (e) => {
        const { name, value } = e.target;

        setForm((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setLoading(true);
        setError("");
        setItinerary(null);

        try {
            const tripData = {
                ...form,
                budget: Number(form.budget),
                travelers: Number(form.travelers),
                interests: form.interests
                    .split(",")
                    .map((item) => item.trim())
                    .filter((item) => item !== ""),
            };

            const createdTrip = await createTrip(tripData);

            console.log("Trip created:", createdTrip);

            setTripId(createdTrip.trip_id);

            const generatedItinerary = await generateItinerary(
                createdTrip.trip_id
            );

            console.log("Itinerary:", generatedItinerary);

            setItinerary(generatedItinerary);
        } catch (err) {
            console.error(err);
            setError(err.message || "Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    const handleDisruption = async () => {
    if (!tripId) {
        setError("Trip ID not found");
        return;
    }

    if (!selectedActivity) {
        setError("Please select an activity");
        return;
    }

    try {
        setLoading(true);
        setError("");

        const result = await simulateDisruption(tripId, {
            type: "activity_cancelled",
            activity: selectedActivity,
        });

        console.log("Replanned itinerary:", result);

        setItinerary(result);
    } catch (err) {
        console.error(err);
        setError(err.message || "Failed to re-plan trip");
    } finally {
        setLoading(false);
    }
};

    return (
        <div className="app">

            <header className="header">
                <h1>TravelPilot</h1>
                <p>
                    AI-powered trip planning and disruption management
                </p>
            </header>

            <main className="container">

                <section className="card">
                    <h2>Create Your Trip</h2>

                    <form onSubmit={handleSubmit}>

                        <label>Destination</label>

                        <input
                            type="text"
                            name="destination"
                            placeholder="e.g. Paris"
                            value={form.destination}
                            onChange={handleChange}
                            required
                        />

                        <div className="row">

                            <div>
                                <label>Start Date</label>

                                <input
                                    type="date"
                                    name="start_date"
                                    value={form.start_date}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div>
                                <label>End Date</label>

                                <input
                                    type="date"
                                    name="end_date"
                                    value={form.end_date}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                        </div>

                        <div className="row">

                            <div>
                                <label>Budget</label>

                                <input
                                    type="number"
                                    name="budget"
                                    placeholder="e.g. 100000"
                                    value={form.budget}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div>
                                <label>Currency</label>

                                <select
                                    name="currency"
                                    value={form.currency}
                                    onChange={handleChange}
                                >
                                    <option value="INR">INR</option>
                                    <option value="USD">USD</option>
                                    <option value="EUR">EUR</option>
                                    <option value="GBP">GBP</option>
                                </select>
                            </div>

                        </div>

                        <label>Number of Travelers</label>

                        <input
                            type="number"
                            name="travelers"
                            min="1"
                            value={form.travelers}
                            onChange={handleChange}
                            required
                        />

                        <label>Interests</label>

                        <input
                            type="text"
                            name="interests"
                            placeholder="History, Food, Architecture"
                            value={form.interests}
                            onChange={handleChange}
                        />

                        <label>Preferences</label>

                        <textarea
                            name="preferences"
                            placeholder="e.g. Prefer museums in the morning"
                            value={form.preferences}
                            onChange={handleChange}
                        />

                        <label>Hotel Name</label>

                        <input
                            type="text"
                            name="hotel_name"
                            placeholder="e.g. Hotel Example"
                            value={form.hotel_name}
                            onChange={handleChange}
                        />

                        <label>Hotel Location</label>

                        <input
                            type="text"
                            name="hotel_location"
                            placeholder="e.g. Central Paris"
                            value={form.hotel_location}
                            onChange={handleChange}
                        />

                        <button type="submit" disabled={loading}>
                            {loading
                                ? "Generating..."
                                : "Generate My Trip"}
                        </button>

                    </form>

                    {error && (
                        <div className="error">
                            {error}
                        </div>
                    )}

                </section>


                {itinerary && (
                    <section className="card itinerary">

                        {/* DISRUPTION CENTER */}

                        <div className="disruption-center">

                              <h2>⚠️ Disruption Center</h2>

                              <p>
                                  Simulate a disruption and let TravelPilot
                                  automatically re-plan your trip.
                              </p>

                              <label>Activity affected</label>

                              <select
                                  value={selectedActivity}
                                  onChange={(e) =>
                                      setSelectedActivity(e.target.value)
                                  }
                              >
                                  <option value="">
                                      Select an activity
                                  </option>

                                  {itinerary.days?.flatMap((day) =>
                                      day.activities?.map((activity) => (
                                          <option
                                              key={activity.name}
                                              value={activity.name}
                                          >
                                              {activity.name}
                                          </option>
                                      ))
                                  )}
                              </select>

                              <button
                                  type="button"
                                  onClick={handleDisruption}
                                  disabled={loading}
                              >
                                  {loading
                                      ? "Re-planning..."
                                      : "Simulate Disruption"}
                              </button>

                          </div>


                        {/* REPLANNING ALERT */}

                        {itinerary.replanned && (
                            <div className="replanned-alert">

                                <h3>
                                    🔄 Trip Replanned
                                </h3>

                                <p>
                                    <strong>
                                        {itinerary.disruption?.activity}
                                    </strong>{" "}
                                    was cancelled.
                                </p>

                                <p>
                                    Replacement:{" "}
                                    <strong>
                                        {itinerary.replacement?.name}
                                    </strong>
                                </p>

                            </div>
                        )}


                        <h2>Your AI Itinerary</h2>


                        {itinerary.trip_summary && (
                            <div className="summary">

                                <h3>
                                    {
                                        itinerary.trip_summary
                                            .destination
                                    }
                                </h3>

                                <p>
                                    {
                                        itinerary.trip_summary
                                            .start_date
                                    }{" "}
                                    →{" "}
                                    {
                                        itinerary.trip_summary
                                            .end_date
                                    }
                                </p>

                                <p>
                                    Travelers:{" "}
                                    {
                                        itinerary.trip_summary
                                            .travelers
                                    }
                                </p>

                            </div>
                        )}


                        {itinerary.days?.map((day, index) => (

                            <div
                                className="day"
                                key={index}
                            >

                                <h3>
                                    {day.date}
                                </h3>


                                {day.activities?.length > 0 ? (

                                    <ul>

                                        {day.activities.map(
                                            (
                                                activity,
                                                activityIndex
                                            ) => (

                                                <li
                                                    key={
                                                        activityIndex
                                                    }
                                                    className="activity-card"
                                                >

                                                    <div className="activity-header">

                                                        <strong>
                                                            {
                                                                activity.name
                                                            }
                                                        </strong>

                                                        {activity.status ===
                                                            "replanned" && (

                                                            <span className="status-badge replanned">
                                                                🔄 REPLANNED
                                                            </span>

                                                        )}

                                                    </div>


                                                    <div className="activity-details">

                                                        {activity.start_time &&
                                                            activity.end_time && (

                                                            <span>
                                                                🕘{" "}
                                                                {
                                                                    activity.start_time
                                                                }{" "}
                                                                –{" "}
                                                                {
                                                                    activity.end_time
                                                                }
                                                            </span>

                                                        )}


                                                        {activity.location && (

                                                            <span>
                                                                📍{" "}
                                                                {
                                                                    activity.location
                                                                }
                                                            </span>

                                                        )}


                                                        {activity.category && (

                                                            <span>
                                                                🏷️{" "}
                                                                {
                                                                    activity.category
                                                                }
                                                            </span>

                                                        )}


                                                        {activity.cost !==
                                                            undefined && (

                                                            <span>
                                                                💰{" "}
                                                                {
                                                                    activity.cost
                                                                }{" "}
                                                                {
                                                                    itinerary
                                                                        .trip_summary
                                                                        ?.currency
                                                                }
                                                            </span>

                                                        )}

                                                    </div>


                                                    {activity.description && (

                                                        <p className="activity-description">
                                                            {
                                                                activity.description
                                                            }
                                                        </p>

                                                    )}

                                                </li>

                                            )
                                        )}

                                    </ul>

                                ) : (

                                    <p>
                                        No activities planned.
                                    </p>

                                )}

                            </div>

                        ))}

                    </section>
                )}

            </main>
        </div>
    );
}

export default App;