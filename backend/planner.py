from datetime import datetime, timedelta


ACTIVITIES = [
    {
        "name": "Louvre Museum",
        "location": "Paris",
        "category": "History",
        "duration": 180,
        "cost": 25,
        "priority": "high"
    },
    {
        "name": "Eiffel Tower",
        "location": "Paris",
        "category": "Architecture",
        "duration": 120,
        "cost": 30,
        "priority": "high"
    },
    {
        "name": "Seine River Cruise",
        "location": "Paris",
        "category": "Relaxation",
        "duration": 90,
        "cost": 20,
        "priority": "medium"
    },
    {
        "name": "Musée d'Orsay",
        "location": "Paris",
        "category": "History",
        "duration": 150,
        "cost": 16,
        "priority": "high"
    },
    {
        "name": "Montmartre",
        "location": "Paris",
        "category": "Architecture",
        "duration": 120,
        "cost": 10,
        "priority": "medium"
    },
    {
        "name": "French Food Tour",
        "location": "Paris",
        "category": "Food",
        "duration": 120,
        "cost": 35,
        "priority": "medium"
    }
]


def generate_itinerary(trip):

    interests = trip["interests"]

    matching = [
        activity
        for activity in ACTIVITIES
        if activity["category"] in interests
    ]

    if not matching:
        matching = ACTIVITIES[:]

    days = []

    current_date = datetime.strptime(
        trip["start_date"],
        "%Y-%m-%d"
    )

    end_date = datetime.strptime(
        trip["end_date"],
        "%Y-%m-%d"
    )

    day_number = 1

    while current_date <= end_date:

        day_activities = []

        selected = matching[(day_number - 1) * 2: day_number * 2]

        current_time = datetime.strptime(
            "09:00",
            "%H:%M"
        )

        for index, activity in enumerate(selected):

            start_time = current_time

            end_time = start_time + timedelta(
                minutes=activity["duration"]
            )

            day_activities.append({
                **activity,
                "start_time": start_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "travel_from_previous": 15 if index > 0 else 0,
                "status": "scheduled"
            })

            current_time = end_time + timedelta(minutes=30)

        daily_cost = sum(
            activity["cost"]
            for activity in day_activities
        )

        days.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "activities": day_activities,
            "daily_cost": daily_cost
        })

        current_date += timedelta(days=1)
        day_number += 1

    total_cost = sum(
        day["daily_cost"]
        for day in days
    )

    return {
        "trip_summary": trip,
        "days": days,
        "total_cost": total_cost,
        "alternatives": [],
        "warnings": []
    }
def replan_itinerary(trip_data, current_itinerary, disruption):
    """
    Re-plan an itinerary using multiple replacement candidates.

    The planner considers:
    - Activity category
    - User interests
    - User preferences
    - Time conflicts
    - Budget
    """

    cancelled_activity = disruption.get("activity")

    # ---------------------------------------------------------
    # Helper: Convert HH:MM to minutes
    # ---------------------------------------------------------

    def time_to_minutes(time_string):
        hours, minutes = map(
            int,
            time_string.split(":")
        )

        return hours * 60 + minutes

    # ---------------------------------------------------------
    # Helper: Check time conflict
    # ---------------------------------------------------------

    def has_time_conflict(candidate, activities):

        candidate_start = time_to_minutes(
            candidate["start_time"]
        )

        candidate_end = time_to_minutes(
            candidate["end_time"]
        )

        for activity in activities:

            if activity.get("name") == cancelled_activity:
                continue

            if (
                not activity.get("start_time")
                or not activity.get("end_time")
            ):
                continue

            activity_start = time_to_minutes(
                activity["start_time"]
            )

            activity_end = time_to_minutes(
                activity["end_time"]
            )

            if (
                candidate_start < activity_end
                and candidate_end > activity_start
            ):
                return True

        return False

    # ---------------------------------------------------------
    # Replacement candidates
    # ---------------------------------------------------------

    replacement_candidates = [

        {
            "name": "Sainte-Chapelle",
            "category": "History",
            "duration": 90,
            "cost": 15,
            "start_time": "09:00",
            "end_time": "10:30",
            "description": (
                "Visit the historic Sainte-Chapelle "
                "and explore its famous stained-glass windows."
            )
        },

        {
            "name": "Notre-Dame Cathedral",
            "category": "History",
            "duration": 90,
            "cost": 0,
            "start_time": "10:30",
            "end_time": "12:00",
            "description": (
                "Explore the historic Notre-Dame Cathedral "
                "and its surrounding area."
            )
        },

        {
            "name": "Arc de Triomphe",
            "category": "Architecture",
            "duration": 90,
            "cost": 16,
            "start_time": "15:00",
            "end_time": "16:30",
            "description": (
                "Explore the Arc de Triomphe "
                "and its surrounding architecture."
            )
        },

        {
            "name": "Montmartre Walking Tour",
            "category": "Architecture",
            "duration": 120,
            "cost": 10,
            "start_time": "14:00",
            "end_time": "16:00",
            "description": (
                "Explore Montmartre and its historic "
                "streets and architecture."
            )
        },

        {
            "name": "Musée de l'Orangerie",
            "category": "Art",
            "duration": 90,
            "cost": 12,
            "start_time": "10:00",
            "end_time": "11:30",
            "description": (
                "Explore impressionist and "
                "post-impressionist artworks."
            )
        },

        {
            "name": "Rodin Museum",
            "category": "Art",
            "duration": 120,
            "cost": 14,
            "start_time": "14:00",
            "end_time": "16:00",
            "description": (
                "Explore sculptures and artworks "
                "at the Rodin Museum."
            )
        },

        {
            "name": "Local French Food Experience",
            "category": "Food",
            "duration": 120,
            "cost": 30,
            "start_time": "12:00",
            "end_time": "14:00",
            "description": (
                "Experience traditional French cuisine "
                "and local dishes."
            )
        },

        {
            "name": "French Bakery Tour",
            "category": "Food",
            "duration": 90,
            "cost": 12,
            "start_time": "16:30",
            "end_time": "18:00",
            "description": (
                "Explore local bakeries and "
                "traditional French pastries."
            )
        }
    ]

    # ---------------------------------------------------------
    # Find cancelled activity
    # ---------------------------------------------------------

    for day in current_itinerary.get("days", []):

        activities = day.get("activities", [])

        for index, activity in enumerate(activities):

            if activity.get("name") != cancelled_activity:
                continue

            cancelled_category = activity.get(
                "category",
                "History"
            )

            # -------------------------------------------------
            # User interests
            # -------------------------------------------------

            interests = trip_data.get(
                "interests",
                []
            )

            interests = [
                str(item).lower()
                for item in interests
            ]

            # -------------------------------------------------
            # Budget information
            # -------------------------------------------------

            trip_budget = float(
                trip_data.get("budget") or 0
            )

            current_total = float(
                current_itinerary.get("total_cost") or 0
            )

            # -------------------------------------------------
            # Score candidates
            # -------------------------------------------------

            scored_candidates = []

            for candidate in replacement_candidates:

                # Don't replace with the same activity
                if candidate["name"] == cancelled_activity:
                    continue

                # Category score
                score = 0

                if (
                    candidate["category"].lower()
                    == cancelled_category.lower()
                ):
                    score += 5

                # Interest score
                if (
                    candidate["category"].lower()
                    in interests
                ):
                    score += 4

                # Time conflict
                if has_time_conflict(
                    candidate,
                    activities
                ):
                    continue

                # Budget check
                new_total = (
                    current_total
                    - activity.get("cost", 0)
                    + candidate["cost"]
                )

                if (
                    trip_budget > 0
                    and new_total > trip_budget
                ):
                    continue

                # Preference score
                preferences = str(
                    trip_data.get("preferences") or ""
                ).lower()

                start_hour = int(
                    candidate["start_time"].split(":")[0]
                )

                if (
                    "morning" in preferences
                    and start_hour < 12
                ):
                    score += 2

                if (
                    "afternoon" in preferences
                    and 12 <= start_hour < 17
                ):
                    score += 2

                if (
                    "evening" in preferences
                    and start_hour >= 17
                ):
                    score += 2

                # Lower cost gets a small bonus
                if candidate["cost"] <= activity.get(
                    "cost",
                    candidate["cost"]
                ):
                    score += 1

                scored_candidates.append(
                    {
                        **candidate,
                        "score": score
                    }
                )

            # -------------------------------------------------
            # No valid replacement
            # -------------------------------------------------

            if not scored_candidates:

                return {
                    **current_itinerary,
                    "replanned": False,
                    "message": (
                        "No suitable replacement was found "
                        "without creating a conflict or "
                        "exceeding the budget."
                    )
                }

            # -------------------------------------------------
            # Select highest-scoring candidate
            # -------------------------------------------------

            scored_candidates.sort(
                key=lambda item: item["score"],
                reverse=True
            )

            replacement = scored_candidates[0].copy()

            replacement["location"] = trip_data.get(
                "destination",
                "Unknown"
            )

            replacement["priority"] = "medium"

            replacement["travel_from_previous"] = activity.get(
                "travel_from_previous",
                15
            )

            replacement["status"] = "replanned"

            # -------------------------------------------------
            # Replace activity
            # -------------------------------------------------

            activities[index] = replacement

            # Sort chronologically
            activities.sort(
                key=lambda item: item.get(
                    "start_time",
                    "00:00"
                )
            )

            # Recalculate daily cost
            day["daily_cost"] = sum(
                item.get("cost", 0)
                for item in activities
            )

            # Recalculate total cost
            total_cost = sum(
                day_item.get("daily_cost", 0)
                for day_item in current_itinerary.get(
                    "days",
                    []
                )
            )

            current_itinerary["total_cost"] = total_cost

            return {
                **current_itinerary,
                "days": current_itinerary["days"],
                "replanned": True,

                "disruption": {
                    "activity": cancelled_activity,
                    "status": "cancelled"
                },

                "replacement": replacement,

                "replacement_score": replacement["score"],

                "candidates_considered": len(
                    scored_candidates
                ),

                "planning_reason": (
                    "Replacement selected using "
                    "category, interests, preferences, "
                    "time conflicts and budget."
                )
            }

    return {
        **current_itinerary,
        "replanned": False,
        "message": (
            "Cancelled activity was not found "
            "in the itinerary."
        )
    }

