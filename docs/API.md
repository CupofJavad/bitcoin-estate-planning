# API Documentation

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.yourdomain.com`

## Authentication

All protected endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <token>
```

### Authentication Endpoints

#### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Response**: `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false
}
```

#### Login

```http
POST /api/v1/auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword123
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### Get Current User

```http
GET /api/v1/auth/users/me
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false
}
```

## Estate Plans

### List Estate Plans

```http
GET /api/v1/estate-plans
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "Main Bitcoin Estate",
    "description": "Primary estate plan",
    "bitcoin_address": "tb1q...",
    "is_active": true,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
]
```

### Get Estate Plan

```http
GET /api/v1/estate-plans/{id}
Authorization: Bearer <token>
```

**Response**: `200 OK` (includes beneficiaries and timelock_policies)

### Create Estate Plan

```http
POST /api/v1/estate-plans
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Estate Plan",
  "description": "Description",
  "bitcoin_address": "tb1q...",
  "is_active": true
}
```

### Update Estate Plan

```http
PATCH /api/v1/estate-plans/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Name"
}
```

### Delete Estate Plan

```http
DELETE /api/v1/estate-plans/{id}
Authorization: Bearer <token>
```

## Beneficiaries

### List Beneficiaries

```http
GET /api/v1/beneficiaries?estate_plan_id={id}
Authorization: Bearer <token>
```

### Create Beneficiary

```http
POST /api/v1/beneficiaries
Authorization: Bearer <token>
Content-Type: application/json

{
  "estate_plan_id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "bitcoin_address": "tb1q...",
  "allocation_percentage": 50.0
}
```

## Timelock Policies

### List Timelock Policies

```http
GET /api/v1/timelock-policies?estate_plan_id={id}
Authorization: Bearer <token>
```

### Create Timelock Policy

```http
POST /api/v1/timelock-policies
Authorization: Bearer <token>
Content-Type: application/json

{
  "estate_plan_id": 1,
  "name": "Death Trigger",
  "description": "Activates on death",
  "timelock_blocks": 1440,
  "trigger_condition": "death",
  "is_active": true
}
```

## Bitcoin

### Validate Address

```http
POST /api/v1/bitcoin/validate
Authorization: Bearer <token>
Content-Type: application/json

{
  "address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
  "network": "testnet"
}
```

**Response**: `200 OK`
```json
{
  "valid": true,
  "format": "bech32",
  "network": "testnet",
  "errors": []
}
```

### Get Balance

```http
GET /api/v1/bitcoin/balance/{address}?use_cache=true
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
{
  "address": "tb1q...",
  "balance_btc": 0.5,
  "balance_sats": 50000000,
  "confirmed": true,
  "cached": false,
  "provider": "blockstream",
  "last_updated": "2025-01-01T00:00:00Z"
}
```

## Chatbot

### Send Message

```http
POST /api/v1/chatbot/chat
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "What is a Bitcoin timelock?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help you?"
    }
  ]
}
```

**Response**: `200 OK`
```json
{
  "response": "A Bitcoin timelock is...",
  "model": "gpt-3.5-turbo",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

### Get Suggestions

```http
GET /api/v1/chatbot/suggestions
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
[
  "What is a Bitcoin timelock?",
  "How do I set up an estate plan?",
  ...
]
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

**Status Codes**:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting

- **API Endpoints**: 10 requests/second per user
- **Bitcoin Balance**: 1 request/second (cached for 5 minutes)
- **Chatbot**: 10 requests/minute per user

## Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
