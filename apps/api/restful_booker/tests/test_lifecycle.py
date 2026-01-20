"""Restful Booker API - Full Lifecycle Tests."""

import allure
import pytest


@allure.epic("Restful Booker API")
@allure.feature("Booking Lifecycle")
@pytest.mark.api
class TestBookingLifecycle:
    """Test suite for complete booking lifecycle."""

    @pytest.fixture
    def sample_booking(self):
        """Sample booking data for testing."""
        return {
            "firstname": "Lifecycle",
            "lastname": "Test",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-02-01",
                "checkout": "2025-02-05"
            },
            "additionalneeds": "WiFi"
        }

    @allure.story("Complete Lifecycle")
    @allure.title("Complete booking lifecycle: Create → Read → Update → Delete")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_complete_booking_lifecycle(self, authenticated_client, sample_booking):
        """
        Test the complete lifecycle of a booking.

        Steps:
        1. Create auth token
        2. Create new booking
        3. Verify booking exists (GET)
        4. Update booking (PUT)
        5. Verify update
        6. Delete booking
        7. Verify deletion (GET returns 404)
        """
        booking_id = None

        try:
            with allure.step("Step 1: Create new booking"):
                created = authenticated_client.create_booking(sample_booking)
                booking_id = created["bookingid"]
                assert booking_id is not None, "Booking ID should be returned"

                allure.attach(
                    str(booking_id),
                    name="Created Booking ID",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("Step 2: Verify booking exists"):
                retrieved = authenticated_client.get_booking(booking_id)
                assert retrieved["firstname"] == sample_booking["firstname"]
                assert retrieved["totalprice"] == sample_booking["totalprice"]

            with allure.step("Step 3: Update booking"):
                updated_data = sample_booking.copy()
                updated_data["totalprice"] = 200
                updated_data["firstname"] = "Updated"

                updated = authenticated_client.update_booking(booking_id, updated_data)
                assert updated["totalprice"] == 200
                assert updated["firstname"] == "Updated"

            with allure.step("Step 4: Verify booking was updated"):
                retrieved_after_update = authenticated_client.get_booking(booking_id)
                assert retrieved_after_update["totalprice"] == 200
                assert retrieved_after_update["firstname"] == "Updated"

            with allure.step("Step 5: Delete booking"):
                success = authenticated_client.delete_booking(booking_id)
                assert success is True, "Deletion should succeed"

            with allure.step("Step 6: Verify booking was deleted"):
                with pytest.raises(Exception):  # Should get 404
                    authenticated_client.get_booking(booking_id)

        except Exception as e:
            # Clean up if test fails
            if booking_id:
                try:
                    authenticated_client.delete_booking(booking_id)
                except Exception:
                    pass  # Ignore cleanup errors
            raise e
