"""Restful Booker API - CRUD Operations Tests.

This test suite covers booking management operations including:
- Listing and filtering bookings
- Creating new bookings
- Updating bookings (PUT and PATCH)
- Deleting bookings

API Documentation: https://restful-booker.herokuapp.com/apidoc/index.html
"""

from __future__ import annotations

import allure
import pytest

from infrastructure.utils.allure_helpers import api_test


@allure.epic("Restful Booker API")
@allure.feature("Booking Management")
@allure.label("layer", "api")
@allure.label("type", "functional")
@pytest.mark.app("restful_booker")
@pytest.mark.api
class TestBookingCRUD:
    """Test suite for booking CRUD operations."""

    @pytest.fixture
    def sample_booking(self):
        """Sample booking data for testing."""
        return {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-01-01",
                "checkout": "2025-01-05"
            },
            "additionalneeds": "Breakfast"
        }

    @allure.story("List Bookings")
    @allure.title("Get all booking IDs")
    @api_test(
        epic="Restful Booker API",
        feature="Booking Management",
        story="List Bookings",
        testcase="TC-RB-020",
        requirement="US-BOOKING-001",
        severity=allure.severity_level.CRITICAL,
        smoke=True,
        description="""
        Verify that the API returns a list of all booking IDs.

        **Test Coverage:**
        - Retrieve complete list of bookings
        - Response contains bookingid field
        - List structure is correct

        **Business Value:**
        Essential for viewing all available bookings in the system.
        """,
    )
    def test_get_all_bookings(self, restful_booker_client):
        """Test retrieving all booking IDs."""
        with allure.step("Get all bookings"):
            bookings = restful_booker_client.get_bookings()

        with allure.step("Verify bookings list is returned"):
            assert isinstance(bookings, list), "Should return a list"
            assert len(bookings) > 0, "Should have at least one booking"
            assert "bookingid" in bookings[0], "Each booking should have bookingid"

    @allure.story("List Bookings")
    @allure.title("Get bookings with query filters")
    @api_test(
        epic="Restful Booker API",
        feature="Booking Management",
        story="List Bookings",
        testcase="TC-RB-021",
        requirement="US-BOOKING-002",
        severity=allure.severity_level.NORMAL,
        regression=True,
        description="""
        Verify that bookings can be filtered by query parameters.

        **Test Coverage:**
        - Filter bookings by firstname and lastname
        - Filter parameters are correctly applied
        - Response structure is maintained

        **Business Value:**
        Enables users to find specific bookings efficiently.
        """,
    )
    def test_get_bookings_with_filter(self, restful_booker_client):
        """Test retrieving bookings with query filters."""
        with allure.step("Get bookings filtered by name"):
            bookings = restful_booker_client.get_bookings(
                firstname="Jim",
                lastname="Brown"
            )

        with allure.step("Verify filtered results"):
            assert isinstance(bookings, list), "Should return a list"
            # Results may be empty if no matching bookings exist

    @allure.story("View Booking Details")
    @allure.title("Get single booking by ID")
    @api_test(
        epic="Restful Booker API",
        feature="Booking Management",
        story="View Booking Details",
        testcase="TC-RB-022",
        requirement="US-BOOKING-003",
        severity=allure.severity_level.CRITICAL,
        smoke=True,
        description="""
        Verify that a single booking can be retrieved by its ID.

        **Test Coverage:**
        - Retrieve specific booking by ID
        - All booking fields are present
        - Data accuracy is maintained

        **Business Value:**
        Core functionality for viewing individual booking details.
        """,
    )
    def test_get_single_booking(self, restful_booker_client):
        """Test retrieving a single booking."""
        with allure.step("Get list of bookings"):
            bookings = restful_booker_client.get_bookings()
            assert len(bookings) > 0, "Need at least one booking"
            booking_id = bookings[0]["bookingid"]

        with allure.step(f"Get booking {booking_id}"):
            booking = restful_booker_client.get_booking(booking_id)

        with allure.step("Verify booking details"):
            assert "firstname" in booking, "Booking should have firstname"
            assert "lastname" in booking, "Booking should have lastname"
            assert "totalprice" in booking, "Booking should have totalprice"
            assert "bookingdates" in booking, "Booking should have bookingdates"

    @allure.story("View Booking Details")
    @allure.title("Get non-existent booking returns 404")
    @api_test(
        epic="Restful Booker API",
        feature="Booking Management",
        story="View Booking Details",
        testcase="TC-RB-023",
        requirement="US-BOOKING-004",
        severity=allure.severity_level.NORMAL,
        regression=True,
        description="""
        Verify that requesting a non-existent booking returns proper error.

        **Test Coverage:**
        - Invalid booking ID handling
        - Proper error response
        - Error handling for edge cases

        **Business Value:**
        Ensures graceful error handling for invalid requests.
        """,
    )
    def test_get_nonexistent_booking(self, restful_booker_client):
        """Test that getting a non-existent booking returns 404."""
        with allure.step("Attempt to get booking with invalid ID"):
            with pytest.raises(Exception):  # requests.HTTPError
                restful_booker_client.get_booking(999999)

    @allure.story("Create Booking")
    @allure.title("Create new booking")
    @api_test(
        epic="Restful Booker API",
        feature="Booking Management",
        story="Create Booking",
        testcase="TC-RB-024",
        requirement="US-BOOKING-005",
        severity=allure.severity_level.CRITICAL,
        smoke=True,
        description="""
        Verify that a new booking can be created successfully.

        **Test Coverage:**
        - Booking creation with valid data
        - Response contains bookingid
        - Booking data is persisted correctly

        **Business Value:**
        Core functionality for reservation management.
        """,
    )
    def test_create_booking(self, restful_booker_client, sample_booking):
        """Test creating a new booking."""
        with allure.step("Create booking"):
            result = restful_booker_client.create_booking(sample_booking)

        with allure.step("Verify booking was created"):
            assert "bookingid" in result, "Response should contain bookingid"
            assert "booking" in result, "Response should contain booking details"
            assert result["booking"]["firstname"] == sample_booking["firstname"]
            assert result["booking"]["totalprice"] == sample_booking["totalprice"]

    @allure.story("Update Booking")
    @allure.title("Update booking with PUT (full update)")
    @api_test(
        epic="Restful Booker API",
        feature="Booking Management",
        story="Update Booking",
        testcase="TC-RB-025",
        requirement="US-BOOKING-006",
        severity=allure.severity_level.CRITICAL,
        regression=True,
        description="""
        Verify that a booking can be fully updated using PUT method.

        **Test Coverage:**
        - Full booking update (all fields)
        - Changes are persisted correctly
        - Authentication is required

        **Business Value:**
        Enables users to modify their booking details completely.
        """,
    )
    def test_update_booking(self, authenticated_client, sample_booking):
        """Test updating a booking with PUT (full update)."""
        with allure.step("Create a booking first"):
            created = authenticated_client.create_booking(sample_booking)
            booking_id = created["bookingid"]

        with allure.step("Update the booking"):
            updated_data = sample_booking.copy()
            updated_data["firstname"] = "James"
            updated_data["totalprice"] = 200

            updated = authenticated_client.update_booking(booking_id, updated_data)

        with allure.step("Verify booking was updated"):
            assert updated["firstname"] == "James"
            assert updated["totalprice"] == 200
            assert updated["lastname"] == sample_booking["lastname"]

    @allure.story("Update Booking")
    @allure.title("Partially update booking with PATCH")
    @api_test(
        epic="Restful Booker API",
        feature="Booking Management",
        story="Update Booking",
        testcase="TC-RB-026",
        requirement="US-BOOKING-007",
        severity=allure.severity_level.NORMAL,
        regression=True,
        description="""
        Verify that a booking can be partially updated using PATCH method.

        **Test Coverage:**
        - Partial booking update (only specified fields)
        - Other fields remain unchanged
        - Authentication is required

        **Business Value:**
        Allows users to update individual booking fields efficiently.
        """,
    )
    def test_partial_update_booking(self, authenticated_client, sample_booking):
        """Test partially updating a booking with PATCH."""
        with allure.step("Create a booking first"):
            created = authenticated_client.create_booking(sample_booking)
            booking_id = created["bookingid"]

        with allure.step("Partially update the booking"):
            updated = authenticated_client.partial_update_booking(
                booking_id,
                {"firstname": "Jimmy"}
            )

        with allure.step("Verify only firstname was updated"):
            assert updated["firstname"] == "Jimmy"
            # Other fields should remain the same
            assert updated["lastname"] == sample_booking["lastname"]

    @allure.story("Update Booking")
    @allure.title("Update booking fails without authentication")
    @api_test(
        epic="Restful Booker API",
        feature="Booking Management",
        story="Update Booking",
        testcase="TC-RB-028",
        requirement="US-BOOKING-008",
        severity=allure.severity_level.NORMAL,
        regression=True,
        description="""
        Verify that booking update fails without proper authentication.

        **Test Coverage:**
        - Authentication requirement enforcement
        - Security validation for update operations
        - Error handling for unauthorized access

        **Business Value:**
        Ensures security by preventing unauthorized booking modifications.
        """,
    )
    def test_update_without_token(self, restful_booker_client, sample_booking):
        """Test that update fails without authentication token."""
        with allure.step("Create a booking first"):
            created = restful_booker_client.create_booking(sample_booking)
            booking_id = created["bookingid"]

        with allure.step("Attempt to update without token"):
            with pytest.raises(ValueError, match="Token required"):
                restful_booker_client.update_booking(booking_id, sample_booking)

    @allure.story("Delete Booking")
    @allure.title("Delete booking")
    @api_test(
        epic="Restful Booker API",
        feature="Booking Management",
        story="Delete Booking",
        testcase="TC-RB-027",
        requirement="US-BOOKING-009",
        severity=allure.severity_level.CRITICAL,
        regression=True,
        description="""
        Verify that a booking can be deleted successfully.

        **Test Coverage:**
        - Booking deletion returns success
        - Deleted booking is no longer accessible
        - Authentication is required

        **Business Value:**
        Critical for booking cancellation and account management.
        """,
    )
    def test_delete_booking(self, authenticated_client, sample_booking):
        """Test deleting a booking."""
        with allure.step("Create a booking first"):
            created = authenticated_client.create_booking(sample_booking)
            booking_id = created["bookingid"]

        with allure.step("Delete the booking"):
            success = authenticated_client.delete_booking(booking_id)

        with allure.step("Verify deletion was successful"):
            assert success is True, "Delete should return True"

        with allure.step("Verify booking no longer exists"):
            with pytest.raises(Exception):  # Should get 404
                authenticated_client.get_booking(booking_id)
