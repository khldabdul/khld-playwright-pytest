"""Restful Booker API - CRUD Operations Tests."""

import allure
import pytest


@allure.epic("Restful Booker API")
@allure.feature("Booking CRUD")
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

    @allure.story("Read Bookings")
    @allure.title("Get all booking IDs")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_get_all_bookings(self, restful_booker_client):
        """Test retrieving all booking IDs."""
        with allure.step("Get all bookings"):
            bookings = restful_booker_client.get_bookings()

        with allure.step("Verify bookings list is returned"):
            assert isinstance(bookings, list), "Should return a list"
            assert len(bookings) > 0, "Should have at least one booking"
            assert "bookingid" in bookings[0], "Each booking should have bookingid"

    @allure.story("Read Bookings")
    @allure.title("Get bookings with filter")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
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

    @allure.story("Read Bookings")
    @allure.title("Get single booking by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
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

    @allure.story("Read Bookings")
    @allure.title("Get non-existent booking returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_get_nonexistent_booking(self, restful_booker_client):
        """Test that getting a non-existent booking returns 404."""
        with allure.step("Attempt to get booking with invalid ID"):
            with pytest.raises(Exception):  # requests.HTTPError
                restful_booker_client.get_booking(999999)

    @allure.story("Create Booking")
    @allure.title("Create new booking")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
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
    @allure.title("Update booking with PUT")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
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
    @allure.title("Partial update booking with PATCH")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
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
    @allure.title("Update fails without token")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
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
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
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
