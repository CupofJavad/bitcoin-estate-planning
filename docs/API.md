# API Documentation

## Base URL

- Development: `http://localhost:8000`
- API Version: `/api/v1`

## Authentication

Currently, the API does not require authentication for MVP. This should be added in future iterations.

## Endpoints

### Estate Plans

#### List Estate Plans
```http
GET /api/v1/estate-plans
```

Query Parameters:
- `user_id` (optional): Filter by user ID

Response:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "My Estate Plan",
    "description": "Primary estate plan",
    "bitcoin_address": "bc1q...",
    "is_active": true,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
]
```

#### Get Estate Plan
```http
GET /api/v1/estate-plans/{id}
```

Response includes beneficiaries and timelock policies:
```json
{
  "id": 1,
  "user_id": 1,
  "name": "My Estate Plan",
  "description": "Primary estate plan",
  "bitcoin_address": "bc1q...",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z",
  "beneficiaries": [...],
  "timelock_policies": [...]
}
```

#### Create Estate Plan
```http
POST /api/v1/estate-plans
Content-Type: application/json

{
  "user_id": 1,
  "name": "My Estate Plan",
  "description": "Primary estate plan",
  "bitcoin_address": "bc1q..."
}
```

#### Update Estate Plan
```http
PATCH /api/v1/estate-plans/{id}
Content-Type: application/json

{
  "name": "Updated Name",
  "is_active": false
}
```

#### Delete Estate Plan
```http
DELETE /api/v1/estate-plans/{id}
```

### Beneficiaries

#### List Beneficiaries
```http
GET /api/v1/beneficiaries
```

Query Parameters:
- `estate_plan_id` (optional): Filter by estate plan ID

#### Get Beneficiary
```http
GET /api/v1/beneficiaries/{id}
```

#### Create Beneficiary
```http
POST /api/v1/beneficiaries
Content-Type: application/json

{
  "estate_plan_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "bitcoin_address": "bc1q...",
  "allocation_percentage": 50.00
}
```

#### Update Beneficiary
```http
PATCH /api/v1/beneficiaries/{id}
Content-Type: application/json

{
  "allocation_percentage": 60.00
}
```

#### Delete Beneficiary
```http
DELETE /api/v1/beneficiaries/{id}
```

### Timelock Policies

#### List Timelock Policies
```http
GET /api/v1/timelock-policies
```

Query Parameters:
- `estate_plan_id` (optional): Filter by estate plan ID

#### Get Timelock Policy
```http
GET /api/v1/timelock-policies/{id}
```

#### Create Timelock Policy
```http
POST /api/v1/timelock-policies
Content-Type: application/json

{
  "estate_plan_id": 1,
  "name": "Death Trigger Policy",
  "description": "Activates after death confirmation",
  "timelock_blocks": 144,
  "trigger_condition": "death"
}
```

#### Update Timelock Policy
```http
PATCH /api/v1/timelock-policies/{id}
Content-Type: application/json

{
  "is_active": false
}
```

#### Delete Timelock Policy
```http
DELETE /api/v1/timelock-policies/{id}
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

Common status codes:
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

