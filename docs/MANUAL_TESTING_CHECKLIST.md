# Manual Testing Checklist

## Quick Test Run (15 minutes)

### Setup
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000 (or 3001)
- [ ] Browser DevTools Console open
- [ ] Browser DevTools Network tab open

---

## Critical Path Testing (Must Work for Demo)

### 1. Estate Plan Creation Flow ⭐
- [ ] Navigate to home page
- [ ] Click "Create Estate Plan"
- [ ] Fill form: Name="Demo Estate Plan", Description="For investor demo"
- [ ] Add Bitcoin address: "bc1qdemo123..."
- [ ] Click "Create"
- [ ] ✅ Verify: Success toast appears
- [ ] ✅ Verify: Estate plan appears in list
- [ ] ✅ Verify: All fields correct
- [ ] ✅ Verify: No console errors
- [ ] ✅ Verify: Network request shows 201 Created

**API Check:**
```bash
curl http://localhost:8000/api/v1/estate-plans | jq '.[] | select(.name=="Demo Estate Plan")'
```

---

### 2. View Estate Plan Details ⭐
- [ ] Click "View Details" on an estate plan
- [ ] ✅ Verify: Page loads without errors
- [ ] ✅ Verify: Estate plan info displayed
- [ ] ✅ Verify: Statistics cards show correct counts
- [ ] ✅ Verify: Beneficiaries section visible (empty)
- [ ] ✅ Verify: Timelock Policies section visible (empty)
- [ ] ✅ Verify: URL is /estate-plans/{id}
- [ ] ✅ Verify: No console errors
- [ ] ✅ Verify: Network request shows 200 OK

**API Check:**
```bash
curl http://localhost:8000/api/v1/estate-plans/1 | jq '.beneficiaries, .timelock_policies'
```

---

### 3. Add Beneficiary Flow ⭐
- [ ] On estate plan detail page, click "Add Beneficiary"
- [ ] Fill form:
  - Name: "Alice Beneficiary"
  - Email: "alice@example.com"
  - Allocation: 50.00
- [ ] Click "Create"
- [ ] ✅ Verify: Success toast
- [ ] ✅ Verify: Beneficiary appears in list
- [ ] ✅ Verify: Allocation chart updates
- [ ] ✅ Verify: Statistics update (beneficiary count, total allocation)
- [ ] ✅ Verify: No console errors

**API Check:**
```bash
curl http://localhost:8000/api/v1/beneficiaries?estate_plan_id=1
```

---

### 4. Add Second Beneficiary (Allocation Validation) ⭐
- [ ] Click "Add Beneficiary" again
- [ ] Fill form:
  - Name: "Bob Beneficiary"
  - Allocation: 60.00 (would exceed 100%)
- [ ] ✅ Verify: Validation error appears
- [ ] ✅ Verify: Max allocation shown (50%)
- [ ] Change allocation to 50.00
- [ ] Click "Create"
- [ ] ✅ Verify: Beneficiary created
- [ ] ✅ Verify: Total allocation = 100%
- [ ] ✅ Verify: Chart shows both beneficiaries

---

### 5. Add Timelock Policy ⭐
- [ ] Click "Add Policy"
- [ ] Fill form:
  - Name: "Death Trigger"
  - Description: "Activates after death confirmation"
  - Blocks: 144
  - Trigger: "death"
- [ ] ✅ Verify: Estimated days shows (~1 day)
- [ ] Click "Create"
- [ ] ✅ Verify: Success toast
- [ ] ✅ Verify: Policy appears in list
- [ ] ✅ Verify: Statistics update
- [ ] ✅ Verify: No console errors

**API Check:**
```bash
curl http://localhost:8000/api/v1/timelock-policies?estate_plan_id=1
```

---

### 6. Edit Operations ⭐
- [ ] Click "Edit" on estate plan → Update name → Save
- [ ] ✅ Verify: Changes saved, list updates
- [ ] Click "Edit" on beneficiary → Update allocation → Save
- [ ] ✅ Verify: Changes saved, chart updates
- [ ] Click "Edit" on policy → Update blocks → Save
- [ ] ✅ Verify: Changes saved, estimated days updates

---

### 7. Delete Operations ⭐
- [ ] Click "Delete" on beneficiary → Confirm
- [ ] ✅ Verify: Beneficiary removed, chart updates
- [ ] Click "Delete" on policy → Confirm
- [ ] ✅ Verify: Policy removed, statistics update
- [ ] Click "Delete" on estate plan → Confirm
- [ ] ✅ Verify: Estate plan removed from list
- [ ] ✅ Verify: Cascade delete works (beneficiaries/policies also deleted)

---

### 8. Search Functionality
- [ ] Type in search box: "Demo"
- [ ] ✅ Verify: List filters correctly
- [ ] Clear search
- [ ] ✅ Verify: All plans shown

---

### 9. Copy Bitcoin Address
- [ ] Find a Bitcoin address
- [ ] Click copy icon
- [ ] ✅ Verify: Success toast
- [ ] Paste in text editor
- [ ] ✅ Verify: Address copied correctly

---

### 10. Error Handling
- [ ] Stop backend server
- [ ] Try to load estate plans
- [ ] ✅ Verify: User-friendly error message
- [ ] ✅ Verify: App doesn't crash
- [ ] Restart backend
- [ ] Refresh page
- [ ] ✅ Verify: Data loads correctly

---

## Edge Cases Testing

### EC-1: Empty States
- [ ] Delete all estate plans
- [ ] ✅ Verify: Empty state message with "Create" button
- [ ] Create estate plan with no beneficiaries
- [ ] View details
- [ ] ✅ Verify: Empty state for beneficiaries section

### EC-2: Form Validation
- [ ] Try to create estate plan with empty name
- [ ] ✅ Verify: Validation error, cannot submit
- [ ] Try to add beneficiary with >100% allocation
- [ ] ✅ Verify: Validation error, max shown

### EC-3: Navigation
- [ ] Use browser back button
- [ ] ✅ Verify: Navigation works correctly
- [ ] Refresh page on detail view
- [ ] ✅ Verify: Data reloads correctly

### EC-4: Loading States
- [ ] Perform slow action (throttle network in DevTools)
- [ ] ✅ Verify: Loading indicator shows
- [ ] ✅ Verify: Buttons disabled during load

---

## Browser Compatibility

Test in:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)

---

## Mobile Responsiveness

- [ ] Open DevTools → Toggle device toolbar
- [ ] Test on mobile viewport (375px width)
- [ ] ✅ Verify: Layout adapts correctly
- [ ] ✅ Verify: Buttons/forms usable
- [ ] ✅ Verify: Charts readable

---

## Performance Checks

- [ ] Page load time < 2 seconds
- [ ] API response time < 500ms
- [ ] No memory leaks (check over time)
- [ ] Smooth animations/transitions

---

## Security Checks

- [ ] No secrets in console logs
- [ ] No sensitive data in network requests (except necessary)
- [ ] CORS configured correctly
- [ ] Input sanitization (XSS prevention)

---

## Test Results Summary

**Date:** _______________  
**Tester:** _______________  
**Environment:** Local Development

### Critical Path Results
- Estate Plan Creation: ✅ / ❌
- View Details: ✅ / ❌
- Add Beneficiary: ✅ / ❌
- Add Policy: ✅ / ❌
- Edit Operations: ✅ / ❌
- Delete Operations: ✅ / ❌
- Search: ✅ / ❌
- Error Handling: ✅ / ❌

### Issues Found
1. ________________________________
2. ________________________________
3. ________________________________

### Notes
________________________________
________________________________

