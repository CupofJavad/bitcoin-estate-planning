# Testing & Debugging Plan - Bitcoin Estate Planning Platform

## Overview
Comprehensive testing plan to verify all frontend-backend connections and user actions work correctly.

## Testing Strategy

### 1. Manual Testing Checklist
Systematic testing of all user stories and edge cases.

### 2. API Integration Testing
Verify all API endpoints respond correctly.

### 3. End-to-End User Flows
Test complete user journeys from start to finish.

### 4. Error Scenario Testing
Test error handling and edge cases.

---

## Test Environment Setup

### Prerequisites
- Backend running on http://localhost:8000
- Frontend running on http://localhost:3000 (or 3001)
- Database with test data
- Browser console open for error inspection

### Test Data Setup
```bash
# Create test estate plans via API or UI
# Ensure at least:
# - 1 estate plan with beneficiaries
# - 1 estate plan with timelock policies
# - 1 empty estate plan
```

---

## Test Cases by User Story

### US-1: Create Estate Plan ✅

**Test Steps:**
1. Navigate to home page
2. Click "Create Estate Plan"
3. Fill in form:
   - Name: "Test Estate Plan 1"
   - Description: "Test description"
   - Bitcoin Address: "bc1qtest123..."
   - Active: checked
4. Click "Create"
5. Verify success toast appears
6. Verify estate plan appears in list
7. Verify all fields are correct

**Expected Results:**
- ✅ Modal opens
- ✅ Form accepts input
- ✅ Success notification appears
- ✅ Estate plan appears in list with correct data
- ✅ Modal closes after save

**API Verification:**
```bash
curl http://localhost:8000/api/v1/estate-plans | jq '.[] | select(.name=="Test Estate Plan 1")'
```

---

### US-2: View Estate Plans List ✅

**Test Steps:**
1. Navigate to home page
2. Verify estate plans are displayed
3. Check that each card shows:
   - Name
   - Description (if present)
   - Status badge
   - Bitcoin address (if present)
   - Created/Updated dates
   - Action buttons

**Expected Results:**
- ✅ All estate plans visible
- ✅ Cards display all information correctly
- ✅ Status badges show correct state (Active/Inactive)
- ✅ Dates formatted correctly

**API Verification:**
```bash
curl http://localhost:8000/api/v1/estate-plans
```

---

### US-3: Edit Estate Plan ✅

**Test Steps:**
1. Click "Edit" on an estate plan card
2. Verify modal opens with pre-filled data
3. Modify name to "Updated Name"
4. Change description
5. Toggle active status
6. Click "Update"
7. Verify success notification
8. Verify changes appear in list

**Expected Results:**
- ✅ Modal opens with correct data
- ✅ Changes are saved
- ✅ List updates immediately
- ✅ Success notification appears

**API Verification:**
```bash
curl http://localhost:8000/api/v1/estate-plans/{id}
```

---

### US-4: Delete Estate Plan ✅

**Test Steps:**
1. Click "Delete" on an estate plan
2. Verify confirmation dialog appears
3. Click "Cancel" - verify nothing happens
4. Click "Delete" again
5. Click "OK" in confirmation
6. Verify success notification
7. Verify estate plan removed from list

**Expected Results:**
- ✅ Confirmation dialog appears
- ✅ Cancel works correctly
- ✅ Delete removes estate plan
- ✅ Success notification appears
- ✅ Associated beneficiaries/policies also deleted (cascade)

**API Verification:**
```bash
curl -X DELETE http://localhost:8000/api/v1/estate-plans/{id}
curl http://localhost:8000/api/v1/estate-plans/{id}  # Should return 404
```

---

### US-5: View Estate Plan Details ✅

**Test Steps:**
1. Click "View Details" on an estate plan
2. Verify navigation to detail page
3. Verify estate plan information displayed
4. Verify statistics cards show correct counts
5. Verify beneficiaries section visible
6. Verify timelock policies section visible
7. Click "Back to Estate Plans"
8. Verify navigation back to list

**Expected Results:**
- ✅ Page loads without errors
- ✅ All information displayed correctly
- ✅ Statistics are accurate
- ✅ Navigation works both ways
- ✅ URL reflects current page (/estate-plans/{id})

**API Verification:**
```bash
curl http://localhost:8000/api/v1/estate-plans/{id}
# Should return estate plan with beneficiaries and timelock_policies arrays
```

---

### US-6: Search Estate Plans ✅

**Test Steps:**
1. Type in search box: "test"
2. Verify list filters to matching plans
3. Type: "nonexistent"
4. Verify empty state message
5. Clear search
6. Verify all plans shown again

**Expected Results:**
- ✅ Search filters in real-time
- ✅ Case-insensitive search
- ✅ Searches name and description
- ✅ Empty state shown when no matches
- ✅ Clearing search shows all plans

---

### US-7: Add Beneficiary ✅

**Test Steps:**
1. Navigate to estate plan detail page
2. Click "Add Beneficiary"
3. Fill form:
   - Name: "John Doe"
   - Email: "john@example.com"
   - Bitcoin Address: "bc1qbeneficiary..."
   - Allocation: 50.00
4. Click "Create"
5. Verify success notification
6. Verify beneficiary appears in list
7. Verify allocation chart updates

**Expected Results:**
- ✅ Modal opens
- ✅ Form accepts input
- ✅ Validation works (0-100%, email format)
- ✅ Beneficiary created successfully
- ✅ Chart updates to show new allocation
- ✅ Statistics update

**API Verification:**
```bash
curl http://localhost:8000/api/v1/beneficiaries?estate_plan_id={id}
```

---

### US-8: Edit Beneficiary ✅

**Test Steps:**
1. Click "Edit" on a beneficiary card
2. Verify modal opens with pre-filled data
3. Change allocation to 60.00
4. Update email
5. Click "Update"
6. Verify success notification
7. Verify changes reflected in card and chart

**Expected Results:**
- ✅ Modal pre-filled correctly
- ✅ Changes saved
- ✅ Chart updates
- ✅ Card shows updated data

---

### US-9: Delete Beneficiary ✅

**Test Steps:**
1. Click "Delete" on a beneficiary
2. Confirm deletion
3. Verify success notification
4. Verify beneficiary removed from list
5. Verify chart updates

**Expected Results:**
- ✅ Confirmation dialog
- ✅ Beneficiary deleted
- ✅ Chart updates
- ✅ Statistics update

---

### US-10: View Beneficiary Allocation Chart ✅

**Test Steps:**
1. Navigate to estate plan with multiple beneficiaries
2. Verify pie chart displays
3. Verify each beneficiary has distinct color
4. Verify chart shows percentages
5. Verify chart is responsive

**Expected Results:**
- ✅ Chart renders correctly
- ✅ Colors are distinct
- ✅ Percentages accurate
- ✅ Chart responsive on resize

---

### US-11: Validate Total Allocation ✅

**Test Steps:**
1. Navigate to estate plan with 50% allocated
2. Click "Add Beneficiary"
3. Try to enter 60% allocation
4. Verify validation error
5. Verify max allocation shown (50%)
6. Enter 50% (valid)
7. Verify can save

**Expected Results:**
- ✅ Validation prevents >100% total
- ✅ Error message clear
- ✅ Max allocation displayed
- ✅ Can save when valid

---

### US-12: Create Timelock Policy ✅

**Test Steps:**
1. Navigate to estate plan detail page
2. Click "Add Policy"
3. Fill form:
   - Name: "Death Trigger Policy"
   - Description: "Activates after death"
   - Blocks: 144
   - Trigger: "death"
   - Active: checked
4. Verify estimated days shown (~1 day)
5. Click "Create"
6. Verify success notification
7. Verify policy appears in list

**Expected Results:**
- ✅ Modal opens
- ✅ Block count calculator works
- ✅ Trigger condition selector works
- ✅ Policy created successfully
- ✅ Statistics update

**API Verification:**
```bash
curl http://localhost:8000/api/v1/timelock-policies?estate_plan_id={id}
```

---

### US-13: Edit Timelock Policy ✅

**Test Steps:**
1. Click "Edit" on a policy
2. Change block count to 288
3. Verify estimated days updates (~2 days)
4. Change trigger condition
5. Click "Update"
6. Verify changes saved

**Expected Results:**
- ✅ Modal pre-filled
- ✅ Block calculator updates
- ✅ Changes saved
- ✅ Card updates

---

### US-14: Delete Timelock Policy ✅

**Test Steps:**
1. Click "Delete" on a policy
2. Confirm deletion
3. Verify policy removed
4. Verify statistics update

**Expected Results:**
- ✅ Confirmation dialog
- ✅ Policy deleted
- ✅ Statistics update

---

### US-17: Copy Bitcoin Address ✅

**Test Steps:**
1. Find a Bitcoin address (estate plan or beneficiary)
2. Click copy icon
3. Verify success notification
4. Paste in text editor
5. Verify address copied correctly

**Expected Results:**
- ✅ Copy icon clickable
- ✅ Success notification
- ✅ Address in clipboard
- ✅ Can paste correctly

---

### US-18: Handle Backend Connection Errors ✅

**Test Steps:**
1. Stop backend server
2. Try to load estate plans list
3. Verify error message appears
4. Verify message is user-friendly
5. Verify app doesn't crash
6. Start backend
7. Refresh page
8. Verify data loads

**Expected Results:**
- ✅ Error message clear and helpful
- ✅ Suggests checking backend
- ✅ No app crash
- ✅ Can recover when backend restarts

---

### US-19: Loading States ✅

**Test Steps:**
1. Perform slow action (create estate plan)
2. Verify loading spinner/skeleton
3. Verify buttons disabled during load
4. Verify loading clears when done

**Expected Results:**
- ✅ Loading indicator visible
- ✅ Buttons disabled
- ✅ Loading clears appropriately

---

### US-20: Form Validation ✅

**Test Steps:**
1. Try to create estate plan with empty name
2. Verify validation error
3. Try to add beneficiary with >100% allocation
4. Verify validation error
5. Try invalid email format
6. Verify validation error
7. Fill all fields correctly
8. Verify can submit

**Expected Results:**
- ✅ Required field validation
- ✅ Allocation validation
- ✅ Email format validation
- ✅ Cannot submit invalid forms
- ✅ Error messages clear

---

### US-21: Success Notifications ✅

**Test Steps:**
1. Create an estate plan
2. Verify success toast appears
3. Verify toast auto-dismisses
4. Click X on toast
5. Verify manual dismiss works

**Expected Results:**
- ✅ Toast appears on success
- ✅ Auto-dismisses after ~5 seconds
- ✅ Can manually dismiss
- ✅ Multiple toasts stack correctly

---

### US-22: View Estate Plan Statistics ✅

**Test Steps:**
1. Navigate to estate plan detail
2. Verify statistics cards show:
   - Beneficiary count
   - Total allocation
   - Policy count
3. Add a beneficiary
4. Verify statistics update

**Expected Results:**
- ✅ Statistics accurate
- ✅ Update in real-time
- ✅ Display correctly

---

### US-23: Navigate Between Pages ✅

**Test Steps:**
1. From list, click "View Details"
2. Verify URL changes to /estate-plans/{id}
3. Click "Back to Estate Plans"
4. Verify URL changes to /
5. Use browser back button
6. Verify navigation works

**Expected Results:**
- ✅ URL updates correctly
- ✅ Navigation works both ways
- ✅ Browser back/forward works
- ✅ State preserved

---

## API Endpoint Testing

### Estate Plans Endpoints

```bash
# List
curl http://localhost:8000/api/v1/estate-plans

# Get with relations
curl http://localhost:8000/api/v1/estate-plans/1

# Create
curl -X POST http://localhost:8000/api/v1/estate-plans \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"name":"Test","description":"Test desc"}'

# Update
curl -X PATCH http://localhost:8000/api/v1/estate-plans/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Name"}'

# Delete
curl -X DELETE http://localhost:8000/api/v1/estate-plans/1
```

### Beneficiaries Endpoints

```bash
# List
curl http://localhost:8000/api/v1/beneficiaries

# List by estate plan
curl http://localhost:8000/api/v1/beneficiaries?estate_plan_id=1

# Create
curl -X POST http://localhost:8000/api/v1/beneficiaries \
  -H "Content-Type: application/json" \
  -d '{"estate_plan_id":1,"name":"John","allocation_percentage":50.00}'

# Update
curl -X PATCH http://localhost:8000/api/v1/beneficiaries/1 \
  -H "Content-Type: application/json" \
  -d '{"allocation_percentage":60.00}'

# Delete
curl -X DELETE http://localhost:8000/api/v1/beneficiaries/1
```

### Timelock Policies Endpoints

```bash
# List
curl http://localhost:8000/api/v1/timelock-policies

# List by estate plan
curl http://localhost:8000/api/v1/timelock-policies?estate_plan_id=1

# Create
curl -X POST http://localhost:8000/api/v1/timelock-policies \
  -H "Content-Type: application/json" \
  -d '{"estate_plan_id":1,"name":"Policy","timelock_blocks":144}'

# Update
curl -X PATCH http://localhost:8000/api/v1/timelock-policies/1 \
  -H "Content-Type: application/json" \
  -d '{"is_active":false}'

# Delete
curl -X DELETE http://localhost:8000/api/v1/timelock-policies/1
```

---

## Error Scenario Testing

### EC-1: Network Timeout
1. Simulate slow network (throttle in DevTools)
2. Perform action
3. Verify timeout handling
4. Verify retry option (if implemented)

### EC-2: Invalid Estate Plan ID
1. Navigate to /estate-plans/99999
2. Verify 404 error message
3. Verify option to return to list

### EC-3: Allocation > 100%
1. Try to set allocation that exceeds 100%
2. Verify validation prevents save
3. Verify clear error message

### EC-4: Backend Unavailable
1. Stop backend
2. Try all major actions
3. Verify error messages
4. Verify app doesn't crash

### EC-5: Invalid Form Data
1. Submit forms with invalid data
2. Verify validation errors
3. Verify cannot submit

---

## Automated Testing Script

Creating a test script to automate API testing:

