# Debugging Checklist - Frontend-Backend Connections

## Systematic Debugging Approach

### Phase 1: API Endpoint Verification

#### Estate Plans Endpoints
- [ ] `GET /api/v1/estate-plans` - Returns 200, valid JSON array
- [ ] `GET /api/v1/estate-plans/{id}` - Returns 200, includes beneficiaries and policies
- [ ] `POST /api/v1/estate-plans` - Creates successfully, returns 201
- [ ] `PATCH /api/v1/estate-plans/{id}` - Updates successfully, returns 200
- [ ] `DELETE /api/v1/estate-plans/{id}` - Deletes successfully, returns 204

#### Beneficiaries Endpoints
- [ ] `GET /api/v1/beneficiaries` - Returns 200, valid JSON array
- [ ] `GET /api/v1/beneficiaries?estate_plan_id={id}` - Filters correctly
- [ ] `GET /api/v1/beneficiaries/{id}` - Returns 200, valid JSON
- [ ] `POST /api/v1/beneficiaries` - Creates successfully, validates allocation
- [ ] `PATCH /api/v1/beneficiaries/{id}` - Updates successfully
- [ ] `DELETE /api/v1/beneficiaries/{id}` - Deletes successfully

#### Timelock Policies Endpoints
- [ ] `GET /api/v1/timelock-policies` - Returns 200, valid JSON array
- [ ] `GET /api/v1/timelock-policies?estate_plan_id={id}` - Filters correctly
- [ ] `GET /api/v1/timelock-policies/{id}` - Returns 200, valid JSON
- [ ] `POST /api/v1/timelock-policies` - Creates successfully
- [ ] `PATCH /api/v1/timelock-policies/{id}` - Updates successfully
- [ ] `DELETE /api/v1/timelock-policies/{id}` - Deletes successfully

### Phase 2: Frontend Action Testing

#### Estate Plans Actions
- [ ] **List Load**: Page loads, fetches estate plans, displays correctly
- [ ] **Create**: Modal opens, form works, submission succeeds, list updates
- [ ] **Edit**: Modal opens with data, form pre-filled, update succeeds
- [ ] **Delete**: Confirmation works, deletion succeeds, list updates
- [ ] **View Details**: Navigation works, page loads, data displays
- [ ] **Search**: Search filters correctly, case-insensitive

#### Beneficiaries Actions
- [ ] **Add**: Modal opens, form validates, creation succeeds, chart updates
- [ ] **Edit**: Modal pre-filled, update succeeds, chart updates
- [ ] **Delete**: Deletion succeeds, chart updates, statistics update
- [ ] **Allocation Validation**: Prevents >100%, shows max available

#### Timelock Policies Actions
- [ ] **Add**: Modal opens, block calculator works, creation succeeds
- [ ] **Edit**: Modal pre-filled, block calculator updates, update succeeds
- [ ] **Delete**: Deletion succeeds, statistics update

### Phase 3: Data Flow Verification

#### Create Flow
1. User fills form → Frontend validates → API call → Backend validates → Database insert → Response → Frontend updates UI

**Checkpoints:**
- [ ] Form validation works
- [ ] API call includes correct data
- [ ] Backend receives data correctly
- [ ] Database stores correctly
- [ ] Response includes created entity
- [ ] Frontend updates list/display

#### Update Flow
1. User clicks edit → Modal opens with data → User modifies → API call → Backend updates → Response → Frontend updates UI

**Checkpoints:**
- [ ] Modal pre-fills correctly
- [ ] API call includes all changes
- [ ] Backend updates correctly
- [ ] Response includes updated entity
- [ ] Frontend reflects changes

#### Delete Flow
1. User clicks delete → Confirmation → API call → Backend deletes → Response → Frontend removes from UI

**Checkpoints:**
- [ ] Confirmation dialog works
- [ ] API call succeeds
- [ ] Backend deletes (and cascades)
- [ ] Frontend removes item
- [ ] Related data updates (charts, stats)

### Phase 4: Error Handling

#### Network Errors
- [ ] Backend offline → Clear error message
- [ ] Timeout → Appropriate handling
- [ ] CORS error → Check CORS config

#### Validation Errors
- [ ] Required fields → Validation works
- [ ] Invalid data types → Backend rejects, frontend shows error
- [ ] Business rules (allocation >100%) → Validation prevents

#### Server Errors
- [ ] 400 Bad Request → Error message shown
- [ ] 404 Not Found → Error message shown
- [ ] 500 Internal Server Error → Error message shown

### Phase 5: Edge Cases

#### Data Edge Cases
- [ ] Empty lists → Empty states display
- [ ] Very long text → Handles gracefully
- [ ] Special characters → Handles correctly
- [ ] Null/undefined values → Handles gracefully

#### User Action Edge Cases
- [ ] Double-click submit → Prevents duplicate
- [ ] Browser back/forward → State preserved
- [ ] Page refresh → Data reloads
- [ ] Multiple tabs → Independent state

#### Concurrent Operations
- [ ] Create while loading list → Handles correctly
- [ ] Edit while another edit in progress → Last write wins or error

---

## Quick Debug Commands

### Check Backend Health
```bash
curl http://localhost:8000/health
```

### Test All Endpoints
```bash
./scripts/test_api.sh
```

### Check Database
```bash
docker exec -it bitcoin-estate-postgres psql -U postgres -d bitcoin_estate -c "SELECT COUNT(*) FROM estate_plans;"
```

### Check Frontend Console
- Open browser DevTools
- Check Console for errors
- Check Network tab for failed requests

### Check Backend Logs
- Check terminal running uvicorn
- Look for error messages
- Check SQLAlchemy query logs

---

## Common Issues & Solutions

### Issue: "Failed to fetch"
**Possible Causes:**
- Backend not running
- CORS misconfiguration
- Wrong API URL
- Network issue

**Debug Steps:**
1. Check backend is running: `curl http://localhost:8000/health`
2. Check CORS config in `backend/app/main.py`
3. Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
4. Check browser Network tab for actual request

### Issue: 500 Internal Server Error
**Possible Causes:**
- Database connection issue
- Missing relationships (selectinload)
- Validation error
- SQL error

**Debug Steps:**
1. Check backend logs
2. Verify database is running
3. Check endpoint code for missing selectinload
4. Verify data format matches schema

### Issue: Data Not Updating
**Possible Causes:**
- Cache issue
- State not refreshing
- API call not made
- Response not processed

**Debug Steps:**
1. Check Network tab - is request made?
2. Check response - is data correct?
3. Check React state - is it updating?
4. Force refresh: `fetchEstatePlans()` called?

### Issue: Form Validation Not Working
**Possible Causes:**
- React Hook Form not configured
- Validation rules missing
- Error display not working

**Debug Steps:**
1. Check form `register` calls
2. Check validation rules
3. Check error display in component
4. Test with browser DevTools

---

## Testing Tools

### Browser DevTools
- **Console**: JavaScript errors
- **Network**: API requests/responses
- **React DevTools**: Component state
- **Application**: Local storage, cookies

### API Testing
- **Swagger UI**: http://localhost:8000/docs
- **curl**: Command-line testing
- **Postman/Insomnia**: GUI API testing
- **Test Script**: `./scripts/test_api.sh`

### Database Testing
- **psql**: Direct database queries
- **pgAdmin**: GUI database tool
- **Alembic**: Migration verification

---

## Success Criteria

All tests pass when:
- ✅ All API endpoints return correct status codes
- ✅ All frontend actions complete successfully
- ✅ Data persists correctly in database
- ✅ UI updates reflect backend changes
- ✅ Error messages are user-friendly
- ✅ Loading states work correctly
- ✅ Form validation prevents invalid submissions
- ✅ No console errors in browser
- ✅ No errors in backend logs

