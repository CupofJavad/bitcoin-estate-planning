#!/bin/bash
# API Integration Testing Script
# Tests all API endpoints for correct responses

set -e

API_URL="${API_URL:-http://localhost:8000}"
BASE_URL="${API_URL}/api/v1"

echo "🧪 Testing Bitcoin Estate Planning Platform API"
echo "API URL: ${API_URL}"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_status=$4
    local description=$5
    
    if [ -z "$expected_status" ]; then
        expected_status=200
    fi
    
    echo -n "Testing: $description... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -L -w "\n%{http_code}" "${BASE_URL}${endpoint}")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -L -w "\n%{http_code}" -X POST "${BASE_URL}${endpoint}" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" = "PATCH" ]; then
        response=$(curl -s -L -w "\n%{http_code}" -X PATCH "${BASE_URL}${endpoint}" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" = "DELETE" ]; then
        response=$(curl -s -L -w "\n%{http_code}" -X DELETE "${BASE_URL}${endpoint}")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected HTTP $expected_status, got $http_code)"
        echo "  Response: $body"
        ((FAILED++))
        return 1
    fi
}

# Health check
echo "=== Health Check ==="
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/health")
HEALTH_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
if [ "$HEALTH_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓ Health check passed${NC} (HTTP $HEALTH_CODE)"
    ((PASSED++))
else
    echo -e "${RED}✗ Health check failed${NC} (HTTP $HEALTH_CODE)"
    ((FAILED++))
fi

# Estate Plans Tests
echo ""
echo "=== Estate Plans API ==="
test_endpoint "GET" "/estate-plans" "" 200 "List estate plans"

# Create test estate plan
CREATE_RESPONSE=$(curl -s -X POST "${BASE_URL}/estate-plans" \
    -H "Content-Type: application/json" \
    -d '{"user_id":1,"name":"API Test Plan","description":"Created by test script"}')

ESTATE_PLAN_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -n "$ESTATE_PLAN_ID" ]; then
    test_endpoint "GET" "/estate-plans/${ESTATE_PLAN_ID}" "" 200 "Get estate plan with relations"
    test_endpoint "PATCH" "/estate-plans/${ESTATE_PLAN_ID}" '{"name":"Updated Test Plan"}' 200 "Update estate plan"
    
    # Beneficiaries Tests
    echo ""
    echo "=== Beneficiaries API ==="
    BENEFICIARY_DATA="{\"estate_plan_id\":${ESTATE_PLAN_ID},\"name\":\"Test Beneficiary\",\"allocation_percentage\":50.00}"
    BENEFICIARY_RESPONSE=$(curl -s -X POST "${BASE_URL}/beneficiaries" \
        -H "Content-Type: application/json" \
        -d "$BENEFICIARY_DATA")
    
    BENEFICIARY_ID=$(echo "$BENEFICIARY_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    
    if [ -n "$BENEFICIARY_ID" ]; then
        test_endpoint "GET" "/beneficiaries?estate_plan_id=${ESTATE_PLAN_ID}" "" 200 "List beneficiaries by estate plan"
        test_endpoint "GET" "/beneficiaries/${BENEFICIARY_ID}" "" 200 "Get beneficiary"
        test_endpoint "PATCH" "/beneficiaries/${BENEFICIARY_ID}" '{"allocation_percentage":60.00}' 200 "Update beneficiary"
    fi
    
    # Timelock Policies Tests
    echo ""
    echo "=== Timelock Policies API ==="
    POLICY_DATA="{\"estate_plan_id\":${ESTATE_PLAN_ID},\"name\":\"Test Policy\",\"timelock_blocks\":144,\"trigger_condition\":\"death\"}"
    POLICY_RESPONSE=$(curl -s -X POST "${BASE_URL}/timelock-policies" \
        -H "Content-Type: application/json" \
        -d "$POLICY_DATA")
    
    POLICY_ID=$(echo "$POLICY_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    
    if [ -n "$POLICY_ID" ]; then
        test_endpoint "GET" "/timelock-policies?estate_plan_id=${ESTATE_PLAN_ID}" "" 200 "List timelock policies by estate plan"
        test_endpoint "GET" "/timelock-policies/${POLICY_ID}" "" 200 "Get timelock policy"
        test_endpoint "PATCH" "/timelock-policies/${POLICY_ID}" '{"is_active":false}' 200 "Update timelock policy"
        
        # Cleanup
        curl -s -X DELETE "${BASE_URL}/timelock-policies/${POLICY_ID}" > /dev/null
    fi
    
    # Cleanup
    if [ -n "$BENEFICIARY_ID" ]; then
        curl -s -X DELETE "${BASE_URL}/beneficiaries/${BENEFICIARY_ID}" > /dev/null
    fi
    curl -s -X DELETE "${BASE_URL}/estate-plans/${ESTATE_PLAN_ID}" > /dev/null
fi

# Error Cases
echo ""
echo "=== Error Cases ==="
test_endpoint "GET" "/estate-plans/99999" "" 404 "Get non-existent estate plan (404)"
test_endpoint "POST" "/estate-plans" '{"invalid":"data"}' 422 "Create estate plan with invalid data (422)"

# Summary
echo ""
echo "=== Test Summary ==="
echo -e "${GREEN}Passed: ${PASSED}${NC}"
echo -e "${RED}Failed: ${FAILED}${NC}"
echo "Total: $((PASSED + FAILED))"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi

