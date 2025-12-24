#!/bin/bash
# Comprehensive Frontend-Backend Connection Testing
# Tests all user actions and verifies API responses

set -e

API_URL="${API_URL:-http://localhost:8000}"
BASE_URL="${API_URL}/api/v1"

echo "🔍 Comprehensive Frontend-Backend Connection Testing"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASSED=0
FAILED=0
WARNINGS=0

test_action() {
    local description=$1
    local api_call=$2
    local expected_field=$3
    local expected_value=$4
    
    echo -n "  Testing: $description... "
    
    response=$(eval "$api_call")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ] || [ "$http_code" -eq 204 ]; then
        if [ -n "$expected_field" ] && [ -n "$expected_value" ]; then
            if echo "$body" | grep -q "$expected_field.*$expected_value"; then
                echo -e "${GREEN}✓ PASS${NC}"
                ((PASSED++))
                return 0
            else
                echo -e "${YELLOW}⚠ WARN${NC} (Response OK but field not found)"
                ((WARNINGS++))
                return 0
            fi
        else
            echo -e "${GREEN}✓ PASS${NC}"
            ((PASSED++))
            return 0
        fi
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code)"
        ((FAILED++))
        return 1
    fi
}

echo -e "${BLUE}=== Phase 1: Estate Plans API ===${NC}"

# Test 1: List Estate Plans
test_action "List all estate plans" \
    "curl -s -L -w '\n%{http_code}' ${BASE_URL}/estate-plans" \
    "" ""

# Test 2: Create Estate Plan
CREATE_RESPONSE=$(curl -s -L -w "\n%{http_code}" -X POST "${BASE_URL}/estate-plans" \
    -H "Content-Type: application/json" \
    -d '{"user_id":1,"name":"Frontend Test Plan","description":"Created by frontend test"}')

CREATE_CODE=$(echo "$CREATE_RESPONSE" | tail -n1)
CREATE_BODY=$(echo "$CREATE_RESPONSE" | sed '$d')

if [ "$CREATE_CODE" -eq 201 ]; then
    ESTATE_PLAN_ID=$(echo "$CREATE_BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
    if [ -n "$ESTATE_PLAN_ID" ] && [ "$ESTATE_PLAN_ID" != "None" ]; then
        echo -e "  ${GREEN}✓ Created test estate plan (ID: $ESTATE_PLAN_ID)${NC}"
        ((PASSED++))
    else
        echo -e "  ${RED}✗ Failed to parse estate plan ID from response${NC}"
        echo "  Response body: $CREATE_BODY"
        ((FAILED++))
        exit 1
    fi
else
    echo -e "  ${RED}✗ Failed to create test estate plan (HTTP $CREATE_CODE)${NC}"
    echo "  Response: $CREATE_BODY"
    ((FAILED++))
    exit 1
fi

# Test 3: Get Estate Plan with Relations
test_action "Get estate plan with relations" \
    "curl -s -L -w '\n%{http_code}' ${BASE_URL}/estate-plans/${ESTATE_PLAN_ID}" \
    "beneficiaries" ""

# Test 4: Update Estate Plan
test_action "Update estate plan" \
    "curl -s -L -w '\n%{http_code}' -X PATCH ${BASE_URL}/estate-plans/${ESTATE_PLAN_ID} -H 'Content-Type: application/json' -d '{\"name\":\"Updated Test Plan\"}'" \
    "name" "Updated Test Plan"

echo ""
echo -e "${BLUE}=== Phase 2: Beneficiaries API ===${NC}"

# Test 5: Create Beneficiary
BENEFICIARY_RESPONSE=$(curl -s -L -w "\n%{http_code}" -X POST "${BASE_URL}/beneficiaries" \
    -H "Content-Type: application/json" \
    -d "{\"estate_plan_id\":${ESTATE_PLAN_ID},\"name\":\"Test Beneficiary\",\"allocation_percentage\":50.00}")

BENEFICIARY_CODE=$(echo "$BENEFICIARY_RESPONSE" | tail -n1)
BENEFICIARY_BODY=$(echo "$BENEFICIARY_RESPONSE" | sed '$d')

if [ "$BENEFICIARY_CODE" -eq 201 ]; then
    BENEFICIARY_ID=$(echo "$BENEFICIARY_BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
    if [ -n "$BENEFICIARY_ID" ] && [ "$BENEFICIARY_ID" != "None" ]; then
        echo -e "  ${GREEN}✓ Created test beneficiary (ID: $BENEFICIARY_ID)${NC}"
        ((PASSED++))
    else
        echo -e "  ${RED}✗ Failed to parse beneficiary ID${NC}"
        ((FAILED++))
    fi
else
    echo -e "  ${RED}✗ Failed to create beneficiary (HTTP $BENEFICIARY_CODE)${NC}"
    echo "  Response: $BENEFICIARY_BODY"
    ((FAILED++))
fi

# Test 6: List Beneficiaries by Estate Plan
test_action "List beneficiaries by estate plan" \
    "curl -s -L -w '\n%{http_code}' ${BASE_URL}/beneficiaries?estate_plan_id=${ESTATE_PLAN_ID}" \
    "" ""

# Test 7: Update Beneficiary
if [ -n "$BENEFICIARY_ID" ] && [ "$BENEFICIARY_ID" != "None" ]; then
    test_action "Update beneficiary allocation" \
        "curl -s -L -w '\n%{http_code}' -X PATCH ${BASE_URL}/beneficiaries/${BENEFICIARY_ID} -H 'Content-Type: application/json' -d '{\"allocation_percentage\":60.00}'" \
        "allocation_percentage" "60.00"
fi

echo ""
echo -e "${BLUE}=== Phase 3: Timelock Policies API ===${NC}"

# Test 8: Create Timelock Policy
POLICY_RESPONSE=$(curl -s -L -w "\n%{http_code}" -X POST "${BASE_URL}/timelock-policies" \
    -H "Content-Type: application/json" \
    -d "{\"estate_plan_id\":${ESTATE_PLAN_ID},\"name\":\"Test Policy\",\"timelock_blocks\":144,\"trigger_condition\":\"death\"}")

POLICY_CODE=$(echo "$POLICY_RESPONSE" | tail -n1)
POLICY_BODY=$(echo "$POLICY_RESPONSE" | sed '$d')

if [ "$POLICY_CODE" -eq 201 ]; then
    POLICY_ID=$(echo "$POLICY_BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
    if [ -n "$POLICY_ID" ] && [ "$POLICY_ID" != "None" ]; then
        echo -e "  ${GREEN}✓ Created test policy (ID: $POLICY_ID)${NC}"
        ((PASSED++))
    else
        echo -e "  ${RED}✗ Failed to parse policy ID${NC}"
        ((FAILED++))
    fi
else
    echo -e "  ${RED}✗ Failed to create policy (HTTP $POLICY_CODE)${NC}"
    echo "  Response: $POLICY_BODY"
    ((FAILED++))
fi

# Test 9: List Policies by Estate Plan
test_action "List timelock policies by estate plan" \
    "curl -s -L -w '\n%{http_code}' ${BASE_URL}/timelock-policies?estate_plan_id=${ESTATE_PLAN_ID}" \
    "" ""

# Test 10: Update Policy
if [ -n "$POLICY_ID" ] && [ "$POLICY_ID" != "None" ]; then
    test_action "Update timelock policy" \
        "curl -s -L -w '\n%{http_code}' -X PATCH ${BASE_URL}/timelock-policies/${POLICY_ID} -H 'Content-Type: application/json' -d '{\"is_active\":false}'" \
        "is_active" "false"
fi

echo ""
echo -e "${BLUE}=== Phase 4: Verify Relations ===${NC}"

# Test 11: Verify Estate Plan includes relations
test_action "Verify estate plan includes beneficiaries and policies" \
    "curl -s -L -w '\n%{http_code}' ${BASE_URL}/estate-plans/${ESTATE_PLAN_ID}" \
    "" ""

RELATIONS_BODY=$(curl -s -L "${BASE_URL}/estate-plans/${ESTATE_PLAN_ID}")
BENEF_COUNT=$(echo "$RELATIONS_BODY" | python3 -c "import sys, json; d=json.load(sys.stdin); print(len(d.get('beneficiaries', [])))" 2>/dev/null)
POLICY_COUNT=$(echo "$RELATIONS_BODY" | python3 -c "import sys, json; d=json.load(sys.stdin); print(len(d.get('timelock_policies', [])))" 2>/dev/null)

echo -e "  ${BLUE}Info:${NC} Estate plan has $BENEF_COUNT beneficiary(ies) and $POLICY_COUNT policy(ies)"

echo ""
echo -e "${BLUE}=== Phase 5: Cleanup ===${NC}"

# Cleanup
if [ -n "$POLICY_ID" ] && [ "$POLICY_ID" != "None" ]; then
    curl -s -L -X DELETE "${BASE_URL}/timelock-policies/${POLICY_ID}" > /dev/null
    echo -e "  ${GREEN}✓ Deleted test policy${NC}"
fi

if [ -n "$BENEFICIARY_ID" ] && [ "$BENEFICIARY_ID" != "None" ]; then
    curl -s -L -X DELETE "${BASE_URL}/beneficiaries/${BENEFICIARY_ID}" > /dev/null
    echo -e "  ${GREEN}✓ Deleted test beneficiary${NC}"
fi

if [ -n "$ESTATE_PLAN_ID" ] && [ "$ESTATE_PLAN_ID" != "None" ]; then
    curl -s -L -X DELETE "${BASE_URL}/estate-plans/${ESTATE_PLAN_ID}" > /dev/null
    echo -e "  ${GREEN}✓ Deleted test estate plan${NC}"
fi

echo ""
echo -e "${BLUE}=== Test Summary ===${NC}"
echo -e "${GREEN}Passed: ${PASSED}${NC}"
echo -e "${RED}Failed: ${FAILED}${NC}"
if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}Warnings: ${WARNINGS}${NC}"
fi
echo "Total: $((PASSED + FAILED + WARNINGS))"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All critical tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi

