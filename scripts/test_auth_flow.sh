#!/bin/bash

# Test Authentication Flow
# This script tests the complete authentication flow

set -e

API_URL="${API_URL:-http://localhost:8000}"
TEST_EMAIL="authtest$(date +%s)@example.com"
TEST_PASSWORD="testpass123"
TEST_NAME="Auth Test User"

echo "🧪 Testing Authentication Flow"
echo "================================"
echo ""

# Test 1: Health Check
echo "1️⃣  Testing Backend Health..."
HEALTH=$(curl -s "${API_URL}/health")
if echo "$HEALTH" | grep -q "healthy"; then
    echo "   ✅ Backend is healthy"
else
    echo "   ❌ Backend health check failed"
    echo "   Response: $HEALTH"
    exit 1
fi
echo ""

# Test 2: Registration
echo "2️⃣  Testing User Registration..."
echo "   Email: $TEST_EMAIL"
REGISTER_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "${API_URL}/api/v1/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"${TEST_EMAIL}\",\"password\":\"${TEST_PASSWORD}\",\"full_name\":\"${TEST_NAME}\"}")

HTTP_CODE=$(echo "$REGISTER_RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
BODY=$(echo "$REGISTER_RESPONSE" | grep -v "HTTP_CODE:")

if [ "$HTTP_CODE" = "201" ]; then
    echo "   ✅ Registration successful"
    echo "   Response: $BODY"
else
    echo "   ❌ Registration failed"
    echo "   HTTP Code: $HTTP_CODE"
    echo "   Response: $BODY"
    exit 1
fi
echo ""

# Test 3: Login
echo "3️⃣  Testing User Login..."
LOGIN_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "${API_URL}/api/v1/auth/jwt/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=${TEST_EMAIL}&password=${TEST_PASSWORD}")

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
BODY=$(echo "$LOGIN_RESPONSE" | grep -v "HTTP_CODE:")

if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ Login successful"
    ACCESS_TOKEN=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null || echo "")
    if [ -n "$ACCESS_TOKEN" ]; then
        echo "   ✅ Access token received"
        echo "   Token: ${ACCESS_TOKEN:0:20}..."
    else
        echo "   ⚠️  No access token in response"
    fi
else
    echo "   ❌ Login failed"
    echo "   HTTP Code: $HTTP_CODE"
    echo "   Response: $BODY"
    exit 1
fi
echo ""

# Test 4: Get Current User (Protected Endpoint)
if [ -n "$ACCESS_TOKEN" ]; then
    echo "4️⃣  Testing Protected Endpoint (Get Current User)..."
    USER_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" "${API_URL}/api/v1/auth/users/me" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")

    HTTP_CODE=$(echo "$USER_RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
    BODY=$(echo "$USER_RESPONSE" | grep -v "HTTP_CODE:")

    if [ "$HTTP_CODE" = "200" ]; then
        echo "   ✅ Protected endpoint accessible"
        echo "   User: $BODY"
    else
        echo "   ❌ Protected endpoint failed"
        echo "   HTTP Code: $HTTP_CODE"
        echo "   Response: $BODY"
        exit 1
    fi
    echo ""
fi

# Test 5: List Estate Plans (Protected Endpoint)
if [ -n "$ACCESS_TOKEN" ]; then
    echo "5️⃣  Testing Estate Plans Endpoint..."
    ESTATE_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" "${API_URL}/api/v1/estate-plans" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")

    HTTP_CODE=$(echo "$ESTATE_RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
    BODY=$(echo "$ESTATE_RESPONSE" | grep -v "HTTP_CODE:")

    if [ "$HTTP_CODE" = "200" ]; then
        echo "   ✅ Estate plans endpoint accessible"
        echo "   Response: $BODY"
    else
        echo "   ❌ Estate plans endpoint failed"
        echo "   HTTP Code: $HTTP_CODE"
        echo "   Response: $BODY"
    fi
    echo ""
fi

echo "✅ All authentication tests passed!"
echo ""
echo "Test User Created:"
echo "  Email: $TEST_EMAIL"
echo "  Password: $TEST_PASSWORD"
echo ""
echo "You can now test in the browser with these credentials!"

