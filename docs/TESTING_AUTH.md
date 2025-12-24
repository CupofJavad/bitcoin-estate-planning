# Testing Authentication - Step by Step

## Quick Test Commands

### 1. Start Services

**Terminal 1 - Infrastructure:**
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning
docker-compose -f infra/docker/docker-compose.yml up -d
```

**Terminal 2 - Backend:**
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 3 - Frontend:**
```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/frontend/client-portal
npm install  # If not already done
npm run dev
```

---

## Test Scenarios

### Test 1: User Registration

1. **Via Frontend:**
   - Navigate to: http://localhost:3000/register
   - Fill form and submit
   - Should redirect to `/login`

2. **Via API:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "testpassword123",
       "full_name": "Test User"
     }'
   ```

**Expected:** Returns user object with `id`, `email`, `is_active`, etc.

---

### Test 2: User Login

1. **Via Frontend:**
   - Navigate to: http://localhost:3000/login
   - Enter credentials
   - Should redirect to `/` (dashboard)

2. **Via API:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/jwt/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=test@example.com&password=testpassword123"
   ```

**Expected:** Returns `{"access_token": "...", "token_type": "bearer"}`

---

### Test 3: Protected Endpoints

**Get Current User:**
```bash
# First login to get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/jwt/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword123" | jq -r '.access_token')

# Use token to access protected endpoint
curl http://localhost:8000/api/v1/auth/users/me \
  -H "Authorization: Bearer $TOKEN"
```

**Expected:** Returns user object

**Without Token (should fail):**
```bash
curl http://localhost:8000/api/v1/auth/users/me
```

**Expected:** `401 Unauthorized`

---

### Test 4: Estate Plans (Protected)

**List Estate Plans (requires auth):**
```bash
curl http://localhost:8000/api/v1/estate-plans \
  -H "Authorization: Bearer $TOKEN"
```

**Expected:** Returns empty array `[]` (no estate plans yet)

**Create Estate Plan:**
```bash
curl -X POST http://localhost:8000/api/v1/estate-plans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Estate Plan",
    "description": "Test plan",
    "bitcoin_address": "bc1qtest",
    "is_active": true
  }'
```

**Expected:** Returns created estate plan with `user_id` automatically set

---

### Test 5: Frontend Flow

1. **Register** → http://localhost:3000/register
2. **Login** → http://localhost:3000/login
3. **Dashboard** → http://localhost:3000/
   - Should show empty estate plans list
   - Should show user email in header
4. **Create Estate Plan** → Click "Create Estate Plan"
   - Fill form and submit
   - Should create and show in list
5. **View Estate Plan** → Click on estate plan
   - Should show details page
   - Should allow adding beneficiaries/policies

---

## Verification

### Backend Health
- [ ] http://localhost:8000/health returns `{"status": "healthy"}`
- [ ] http://localhost:8000/docs loads Swagger UI
- [ ] Auth endpoints visible in Swagger UI

### Frontend Health
- [ ] http://localhost:3000 loads
- [ ] Redirects to `/login` if not authenticated
- [ ] Can register new user
- [ ] Can login with registered user
- [ ] Dashboard loads after login
- [ ] User email shown in header
- [ ] Logout button works

### Database
- [ ] `users` table exists
- [ ] Can query users: `SELECT * FROM users;`
- [ ] Estate plans have correct `user_id`

---

## Common Issues & Solutions

### Issue: "401 Unauthorized" on all endpoints
**Solution:** 
- Check token is being sent: `Authorization: Bearer <token>`
- Verify token hasn't expired (30 minutes default)
- Re-login to get new token

### Issue: "Failed to fetch" in frontend
**Solution:**
- Check backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Check CORS settings in backend `.env`

### Issue: Redirect loop on login
**Solution:**
- Check `NEXTAUTH_URL` in frontend `.env.local`
- Clear browser cookies
- Check middleware configuration

### Issue: "Table 'users' does not exist"
**Solution:**
- Run migration: `alembic upgrade head`
- Check database connection

---

**Last Updated**: December 2024

