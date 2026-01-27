"""Restful Booker API - Full Lifecycle Tests.

This test suite covers complete booking lifecycle operations:
- Create → Read → Update → Delete (CRUD)
- End-to-end workflow validation
- Cleanup on failure

API Documentation: https://restful-booker.herokuapp.com/apidoc/index.html
"""

from __future__ import annotations

import allure
import pytest

from infrastructure.utils.allure_helpers import markdown_to_html


@allure.epic("Restful Booker API")
@allure.feature("Booking Lifecycle")
@allure.label("layer", "api")
@allure.label("type", "functional")
@pytest.mark.app("restful_booker")
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
    @allure.title("Complete CRUD lifecycle: Create → Read → Update → Delete")
    @allure.description_html(markdown_to_html("""
    Verify the complete lifecycle of a booking from creation to deletion.

    **Test Steps:**
    1. Create new booking
    2. Verify booking exists (GET)
    3. Update booking (PUT)
    4. Verify update was persisted
    5. Delete booking
    6. Verify deletion (GET returns 404)

    **Test Coverage:**
    - End-to-end booking workflow
    - Data persistence across operations
    - Proper cleanup and resource management

    **Business Value:**
    Validates the complete user journey for booking management.
    """))
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.testcase("TC-RB-030")
    @pytest.mark.requirement("US-LIFECYCLE-001")
    @pytest.mark.smoke
    def test_complete_booking_lifecycle(self, authenticated_client, sample_booking):
        """Test the complete lifecycle of a booking."""
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
