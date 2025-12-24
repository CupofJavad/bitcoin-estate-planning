# User Stories - Bitcoin Estate Planning Platform

## User Story Format
Following industry standards (INVEST principles + Given/When/Then acceptance criteria):

**Format:**
- **As a** [user type]
- **I want** [goal/action]
- **So that** [benefit/value]

**Acceptance Criteria:**
- **Given** [initial context]
- **When** [action/trigger]
- **Then** [expected outcome]

---

## User Personas

1. **Primary User (Estate Owner)**: Individual planning their Bitcoin estate
2. **Beneficiary**: Person who will inherit Bitcoin assets
3. **Estate Administrator**: Person managing multiple estates
4. **Investor/Demo Viewer**: Evaluating the platform

---

## Epic 1: Estate Plan Management

### US-1: Create Estate Plan
**As a** estate owner  
**I want** to create a new estate plan  
**So that** I can organize my Bitcoin inheritance planning

**Acceptance Criteria:**
- **Given** I am on the estate plans page
- **When** I click "Create Estate Plan" and fill in the required fields (name)
- **Then** a new estate plan is created and appears in the list
- **And** I can optionally add a description and Bitcoin address
- **And** the estate plan is set to active by default
- **And** I see a success notification

**Priority:** P0 (Critical)  
**Estimate:** 2 points

---

### US-2: View Estate Plans List
**As a** estate owner  
**I want** to see all my estate plans in a list  
**So that** I can quickly find and manage them

**Acceptance Criteria:**
- **Given** I have one or more estate plans
- **When** I visit the home page
- **Then** I see all my estate plans displayed as cards
- **And** each card shows name, description, status, and Bitcoin address
- **And** I can see creation and update dates
- **And** I can search/filter estate plans by name or description

**Priority:** P0 (Critical)  
**Estimate:** 1 point

---

### US-3: Edit Estate Plan
**As a** estate owner  
**I want** to edit an existing estate plan  
**So that** I can update information as my situation changes

**Acceptance Criteria:**
- **Given** I have an existing estate plan
- **When** I click the "Edit" button on an estate plan card
- **Then** a modal opens with the current values pre-filled
- **And** I can modify name, description, Bitcoin address, and active status
- **And** when I save, the changes are persisted
- **And** I see a success notification
- **And** the updated information appears in the list

**Priority:** P0 (Critical)  
**Estimate:** 2 points

---

### US-4: Delete Estate Plan
**As a** estate owner  
**I want** to delete an estate plan  
**So that** I can remove plans I no longer need

**Acceptance Criteria:**
- **Given** I have an existing estate plan
- **When** I click the "Delete" button
- **Then** I see a confirmation dialog
- **And** when I confirm, the estate plan is deleted
- **And** all associated beneficiaries and timelock policies are also deleted (cascade)
- **And** the estate plan disappears from the list
- **And** I see a success notification

**Priority:** P1 (High)  
**Estimate:** 2 points

---

### US-5: View Estate Plan Details
**As a** estate owner  
**I want** to view detailed information about an estate plan  
**So that** I can see all beneficiaries, policies, and statistics

**Acceptance Criteria:**
- **Given** I have an estate plan
- **When** I click "View Details"
- **Then** I see a detail page with:
  - Estate plan information
  - Statistics (beneficiary count, total allocation, policy count)
  - Beneficiaries list with allocation chart
  - Timelock policies list
- **And** I can navigate back to the estate plans list

**Priority:** P0 (Critical)  
**Estimate:** 3 points

---

### US-6: Search Estate Plans
**As a** estate owner  
**I want** to search my estate plans  
**So that** I can quickly find specific plans

**Acceptance Criteria:**
- **Given** I have multiple estate plans
- **When** I type in the search box
- **Then** the list filters to show only matching plans
- **And** the search matches against name and description
- **And** the search is case-insensitive
- **And** if no matches, I see an appropriate message

**Priority:** P1 (High)  
**Estimate:** 1 point

---

## Epic 2: Beneficiary Management

### US-7: Add Beneficiary
**As a** estate owner  
**I want** to add a beneficiary to an estate plan  
**So that** I can specify who will inherit my Bitcoin

**Acceptance Criteria:**
- **Given** I am viewing an estate plan detail page
- **When** I click "Add Beneficiary" and fill in the form
- **Then** I can enter name (required), email (optional), Bitcoin address (optional), and allocation percentage
- **And** the form validates that allocation percentage is between 0-100
- **And** the form shows remaining available allocation
- **And** when I save, the beneficiary is added
- **And** the allocation chart updates to show the new beneficiary
- **And** I see a success notification

**Priority:** P0 (Critical)  
**Estimate:** 3 points

---

### US-8: Edit Beneficiary
**As a** estate owner  
**I want** to edit a beneficiary's information  
**So that** I can update their details or allocation

**Acceptance Criteria:**
- **Given** I have a beneficiary in an estate plan
- **When** I click "Edit" on a beneficiary card
- **Then** a modal opens with current values pre-filled
- **And** I can modify name, email, Bitcoin address, and allocation percentage
- **And** the allocation validation accounts for the current beneficiary's existing allocation
- **And** when I save, changes are persisted
- **And** the allocation chart updates
- **And** I see a success notification

**Priority:** P0 (Critical)  
**Estimate:** 2 points

---

### US-9: Delete Beneficiary
**As a** estate owner  
**I want** to remove a beneficiary  
**So that** I can update my estate plan

**Acceptance Criteria:**
- **Given** I have a beneficiary in an estate plan
- **When** I click "Delete" on a beneficiary card
- **Then** I see a confirmation dialog
- **And** when I confirm, the beneficiary is removed
- **And** the allocation chart updates
- **And** I see a success notification

**Priority:** P1 (High)  
**Estimate:** 1 point

---

### US-10: View Beneficiary Allocation Chart
**As a** estate owner  
**I want** to see a visual representation of beneficiary allocations  
**So that** I can quickly understand the distribution

**Acceptance Criteria:**
- **Given** I have beneficiaries in an estate plan
- **When** I view the estate plan detail page
- **Then** I see a pie chart showing allocation percentages
- **And** each beneficiary has a distinct color
- **And** the chart shows percentages and names
- **And** the chart is responsive and readable

**Priority:** P1 (High)  
**Estimate:** 2 points

---

### US-11: Validate Total Allocation
**As a** estate owner  
**I want** the system to prevent me from allocating more than 100%  
**So that** my estate plan is mathematically correct

**Acceptance Criteria:**
- **Given** I am adding or editing a beneficiary
- **When** I enter an allocation percentage that would exceed 100% total
- **Then** I see a validation error
- **And** the form shows the maximum allowed allocation
- **And** I cannot save until the allocation is valid
- **And** the form shows remaining available allocation

**Priority:** P0 (Critical)  
**Estimate:** 2 points

---

## Epic 3: Timelock Policy Management

### US-12: Create Timelock Policy
**As a** estate owner  
**I want** to create a timelock policy  
**So that** I can specify when Bitcoin should be released

**Acceptance Criteria:**
- **Given** I am viewing an estate plan detail page
- **When** I click "Add Policy" and fill in the form
- **Then** I can enter policy name (required), description, block count, trigger condition, and active status
- **And** the form shows estimated duration in days based on block count
- **And** I can select from predefined trigger conditions (death, inactivity, manual, date)
- **And** when I save, the policy is created
- **And** I see a success notification

**Priority:** P0 (Critical)  
**Estimate:** 3 points

---

### US-13: Edit Timelock Policy
**As a** estate owner  
**I want** to edit a timelock policy  
**So that** I can adjust the policy as needed

**Acceptance Criteria:**
- **Given** I have a timelock policy
- **When** I click "Edit" on a policy card
- **Then** a modal opens with current values pre-filled
- **And** I can modify all fields including block count and trigger condition
- **And** the estimated duration updates as I change block count
- **And** when I save, changes are persisted
- **And** I see a success notification

**Priority:** P0 (Critical)  
**Estimate:** 2 points

---

### US-14: Delete Timelock Policy
**As a** estate owner  
**I want** to delete a timelock policy  
**So that** I can remove policies I no longer need

**Acceptance Criteria:**
- **Given** I have a timelock policy
- **When** I click "Delete" on a policy card
- **Then** I see a confirmation dialog
- **And** when I confirm, the policy is deleted
- **And** I see a success notification

**Priority:** P1 (High)  
**Estimate:** 1 point

---

### US-15: Toggle Policy Active Status
**As a** estate owner  
**I want** to activate or deactivate a timelock policy  
**So that** I can control which policies are active

**Acceptance Criteria:**
- **Given** I have a timelock policy
- **When** I edit the policy and toggle the "Active" checkbox
- **Then** the status is saved
- **And** the policy card shows the correct status (Active/Inactive)
- **And** I see a success notification

**Priority:** P1 (High)  
**Estimate:** 1 point

---

### US-16: View Block Count Calculator
**As a** estate owner  
**I want** to see how many days a block count represents  
**So that** I can set appropriate timelock periods

**Acceptance Criteria:**
- **Given** I am creating or editing a timelock policy
- **When** I enter a block count
- **Then** I see an estimated duration display (e.g., "~10 days")
- **And** the calculation is based on ~144 blocks per day
- **And** the estimate updates as I change the block count

**Priority:** P1 (High)  
**Estimate:** 1 point

---

## Epic 4: User Experience & Error Handling

### US-17: Copy Bitcoin Address
**As a** estate owner  
**I want** to copy a Bitcoin address to clipboard  
**So that** I can easily share or use it elsewhere

**Acceptance Criteria:**
- **Given** I am viewing an estate plan or beneficiary with a Bitcoin address
- **When** I click the copy icon next to the address
- **Then** the address is copied to my clipboard
- **And** I see a success notification confirming the copy

**Priority:** P1 (High)  
**Estimate:** 1 point

---

### US-18: Handle Backend Connection Errors
**As a** user  
**I want** clear error messages when the backend is unavailable  
**So that** I understand what went wrong

**Acceptance Criteria:**
- **Given** the backend API is not running or unreachable
- **When** I perform any action that requires the API
- **Then** I see a user-friendly error message
- **And** the message suggests checking if the backend is running
- **And** the error doesn't crash the application

**Priority:** P0 (Critical)  
**Estimate:** 2 points

---

### US-19: Loading States
**As a** user  
**I want** to see loading indicators during API calls  
**So that** I know the system is working

**Acceptance Criteria:**
- **Given** I perform an action that requires an API call
- **When** the request is in progress
- **Then** I see a loading spinner or skeleton
- **And** buttons are disabled during submission
- **And** the loading state clears when the request completes

**Priority:** P1 (High)  
**Estimate:** 1 point

---

### US-20: Form Validation
**As a** user  
**I want** real-time validation feedback on forms  
**So that** I can correct errors before submitting

**Acceptance Criteria:**
- **Given** I am filling out a form
- **When** I enter invalid data
- **Then** I see validation errors immediately or on blur
- **And** required fields are clearly marked
- **And** I cannot submit until all validations pass
- **And** error messages are clear and helpful

**Priority:** P0 (Critical)  
**Estimate:** 2 points

---

### US-21: Success Notifications
**As a** user  
**I want** confirmation when actions succeed  
**So that** I know my changes were saved

**Acceptance Criteria:**
- **Given** I perform a successful action (create, update, delete)
- **When** the action completes successfully
- **Then** I see a toast notification with a success message
- **And** the notification auto-dismisses after a few seconds
- **And** I can manually dismiss it

**Priority:** P1 (High)  
**Estimate:** 1 point

---

## Epic 5: Data Display & Navigation

### US-22: View Estate Plan Statistics
**As a** estate owner  
**I want** to see summary statistics for an estate plan  
**So that** I can quickly understand the plan's status

**Acceptance Criteria:**
- **Given** I am viewing an estate plan detail page
- **When** the page loads
- **Then** I see statistics cards showing:
  - Number of beneficiaries
  - Total allocation percentage
  - Number of timelock policies
- **And** the statistics update when I add/remove beneficiaries or policies

**Priority:** P1 (High)  
**Estimate:** 1 point

---

### US-23: Navigate Between Pages
**As a** user  
**I want** to navigate between the estate plans list and detail pages  
**So that** I can move through the application easily

**Acceptance Criteria:**
- **Given** I am on the estate plans list page
- **When** I click "View Details" on an estate plan
- **Then** I navigate to the detail page
- **And** I can click "Back to Estate Plans" to return
- **And** the URL reflects the current page

**Priority:** P0 (Critical)  
**Estimate:** 1 point

---

### US-24: Empty States
**As a** user  
**I want** helpful messages when there's no data  
**So that** I know what to do next

**Acceptance Criteria:**
- **Given** I have no estate plans, beneficiaries, or policies
- **When** I view the respective list
- **Then** I see a friendly empty state message
- **And** I see a call-to-action button to create the first item
- **And** the message is encouraging, not error-like

**Priority:** P1 (High)  
**Estimate:** 1 point

---

## Edge Cases & Error Scenarios

### EC-1: Network Timeout
**Scenario:** API request times out  
**Expected:** User sees timeout error message, can retry

### EC-2: Invalid Estate Plan ID
**Scenario:** User navigates to non-existent estate plan  
**Expected:** 404 error message, option to return to list

### EC-3: Concurrent Updates
**Scenario:** Multiple users edit same estate plan  
**Expected:** Last write wins, or optimistic locking

### EC-4: Large Allocation Percentages
**Scenario:** User enters allocation > 100%  
**Expected:** Validation prevents save, shows error

### EC-5: Special Characters in Names
**Scenario:** User enters special characters in names  
**Expected:** System handles gracefully, sanitizes if needed

### EC-6: Very Long Descriptions
**Scenario:** User enters very long text  
**Expected:** System handles or truncates appropriately

### EC-7: Invalid Bitcoin Address Format
**Scenario:** User enters invalid Bitcoin address  
**Expected:** System accepts (validation can be added later) or shows warning

### EC-8: Browser Back/Forward
**Scenario:** User uses browser navigation  
**Expected:** Application state is preserved correctly

---

## Testing Priority Matrix

### P0 (Critical - Must Test Before Demo)
- US-1: Create Estate Plan
- US-2: View Estate Plans List
- US-3: Edit Estate Plan
- US-5: View Estate Plan Details
- US-7: Add Beneficiary
- US-8: Edit Beneficiary
- US-12: Create Timelock Policy
- US-18: Handle Backend Connection Errors
- US-20: Form Validation
- US-23: Navigate Between Pages

### P1 (High - Should Test)
- US-4: Delete Estate Plan
- US-6: Search Estate Plans
- US-9: Delete Beneficiary
- US-10: View Beneficiary Allocation Chart
- US-11: Validate Total Allocation
- US-13: Edit Timelock Policy
- US-14: Delete Timelock Policy
- US-17: Copy Bitcoin Address
- US-19: Loading States
- US-21: Success Notifications
- US-22: View Estate Plan Statistics

### P2 (Medium - Nice to Have)
- US-15: Toggle Policy Active Status
- US-16: View Block Count Calculator
- US-24: Empty States

---

## User Story Summary

**Total Stories:** 24  
**P0 Stories:** 10  
**P1 Stories:** 11  
**P2 Stories:** 3

**Estimated Total Points:** ~35 points

