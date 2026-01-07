import pytest
from httpx import AsyncClient, ASGITransport
from main import app
import random

@pytest.mark.anyio
async def test_driver():
    # unique email per test run
    email = f"test{random.randint(1, 10000)}@gmail.com"
    name=f"test{random.randint(1,1000)}"
    payload = {
        "driver_name": name,
        "driver_bike_no": "KA01AB1234",
        "driver_license_no": "DL1234567890",
        "driver_phone_no": 9876543210,
        "driver_email": email,
        "driver_password": "password123",
        "driver_password_confirm": "password123",
        "driver_address": "123 Street, City",
        "driver_lat": 12.9716,
        "driver_long": 77.5946
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as sc:
        # Signup
        response = await sc.post('/driver/signup', json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "driver_id" in data
        assert data["message"] == "Driver created successfully"

        # Login
        login_data = {
            "username": payload['driver_email'],
            "password": payload["driver_password"]
        }
        response = await sc.post("/driver/login", data=login_data)
        assert response.status_code == 200
        result = response.json()
        access_token = result["access_token"]
        assert "access_token" in result
        assert result["token_type"] == "bearer"
        assert result["message"] == "Login successful"
        assert result["driver_name"] == payload["driver_name"]

        # Current driver
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await sc.get('/driver/current_driver', headers=headers)
        assert response.status_code == 200
        result = response.json()
        assert result["driver_name"] == payload["driver_name"]

        #update_location
        payloads={
            "driver_lat": 13.0827,
  "driver_long": 80.2707
        }
        response=await sc.put('/driver/update_location',headers=headers,json=payloads)
        assert response.status_code==200
        res=response.json()
        assert res['message']=="Location updated successfully"
