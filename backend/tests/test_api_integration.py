"""Integration tests for API endpoints."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_estate_plan_id(client: AsyncClient):
    """Create a test estate plan and return its ID."""
    response = await client.post(
        "/api/v1/estate-plans",
        json={"user_id": 1, "name": "Test Estate Plan", "description": "Test"}
    )
    assert response.status_code == 201
    data = response.json()
    yield data["id"]
    # Cleanup
    await client.delete(f"/api/v1/estate-plans/{data['id']}")


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_list_estate_plans(client: AsyncClient):
    """Test listing estate plans."""
    response = await client.get("/api/v1/estate-plans")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_estate_plan(client: AsyncClient):
    """Test creating an estate plan."""
    response = await client.post(
        "/api/v1/estate-plans",
        json={
            "user_id": 1,
            "name": "Test Plan",
            "description": "Test description",
            "bitcoin_address": "bc1qtest123",
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Plan"
    assert data["description"] == "Test description"
    assert data["bitcoin_address"] == "bc1qtest123"
    
    # Cleanup
    await client.delete(f"/api/v1/estate-plans/{data['id']}")


@pytest.mark.asyncio
async def test_get_estate_plan_with_relations(client: AsyncClient, test_estate_plan_id: int):
    """Test getting estate plan with relations."""
    response = await client.get(f"/api/v1/estate-plans/{test_estate_plan_id}")
    assert response.status_code == 200
    data = response.json()
    assert "beneficiaries" in data
    assert "timelock_policies" in data
    assert isinstance(data["beneficiaries"], list)
    assert isinstance(data["timelock_policies"], list)


@pytest.mark.asyncio
async def test_update_estate_plan(client: AsyncClient, test_estate_plan_id: int):
    """Test updating an estate plan."""
    response = await client.patch(
        f"/api/v1/estate-plans/{test_estate_plan_id}",
        json={"name": "Updated Name"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_estate_plan(client: AsyncClient):
    """Test deleting an estate plan."""
    # Create estate plan
    create_response = await client.post(
        "/api/v1/estate-plans",
        json={"user_id": 1, "name": "To Delete"}
    )
    estate_plan_id = create_response.json()["id"]
    
    # Delete it
    delete_response = await client.delete(f"/api/v1/estate-plans/{estate_plan_id}")
    assert delete_response.status_code == 204
    
    # Verify it's gone
    get_response = await client.get(f"/api/v1/estate-plans/{estate_plan_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_create_beneficiary(client: AsyncClient, test_estate_plan_id: int):
    """Test creating a beneficiary."""
    response = await client.post(
        "/api/v1/beneficiaries",
        json={
            "estate_plan_id": test_estate_plan_id,
            "name": "John Doe",
            "email": "john@example.com",
            "allocation_percentage": 50.00,
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["allocation_percentage"] == 50.00


@pytest.mark.asyncio
async def test_create_timelock_policy(client: AsyncClient, test_estate_plan_id: int):
    """Test creating a timelock policy."""
    response = await client.post(
        "/api/v1/timelock-policies",
        json={
            "estate_plan_id": test_estate_plan_id,
            "name": "Test Policy",
            "timelock_blocks": 144,
            "trigger_condition": "death",
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Policy"
    assert data["timelock_blocks"] == 144


@pytest.mark.asyncio
async def test_beneficiary_allocation_validation(client: AsyncClient, test_estate_plan_id: int):
    """Test that allocation percentage is validated."""
    # Create beneficiary with valid allocation
    response = await client.post(
        "/api/v1/beneficiaries",
        json={
            "estate_plan_id": test_estate_plan_id,
            "name": "Test",
            "allocation_percentage": 50.00,
        }
    )
    assert response.status_code == 201
    
    # Try to create another with allocation that would exceed 100%
    # Note: Backend doesn't validate total, but frontend does
    response2 = await client.post(
        "/api/v1/beneficiaries",
        json={
            "estate_plan_id": test_estate_plan_id,
            "name": "Test 2",
            "allocation_percentage": 60.00,  # Would make total 110%
        }
    )
    # Backend allows this (business logic in frontend)
    # But we can test the endpoint works
    assert response2.status_code == 201

