# Demo Data Seeding Script

## Overview

The `seed_demo_data.py` script creates sample data for demonstration purposes, including:
- Demo user account
- Sample estate plans
- Sample beneficiaries
- Sample timelock policies

## Usage

### Prerequisites

1. Database must be running and accessible
2. Environment variables must be configured (`.env` file)
3. Database migrations must be applied

### Run the Script

```bash
cd backend
source .venv/bin/activate
python scripts/seed_demo_data.py
```

Or using Python directly:

```bash
cd backend
python3 scripts/seed_demo_data.py
```

### Demo User Credentials

After running the script, you can log in with:

- **Email**: `demo@example.com`
- **Password**: `demo123456`

## What Gets Created

### Estate Plans

1. **Main Bitcoin Estate** (Active)
   - Bitcoin address: `tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx`
   - 3 beneficiaries (50%, 30%, 20% allocation)
   - 2 timelock policies

2. **Family Trust Estate** (Active)
   - Bitcoin address: `tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0slvdk`
   - 2 beneficiaries (60%, 40% allocation)
   - 1 timelock policy

3. **Charitable Giving Plan** (Inactive)
   - No Bitcoin address
   - No beneficiaries or policies

### Beneficiaries

- Alice Johnson (50% of Main Bitcoin Estate)
- Bob Smith (30% of Main Bitcoin Estate)
- Charlie Brown (20% of Main Bitcoin Estate)
- Diana Prince (60% of Family Trust Estate)
- Edward Norton (40% of Family Trust Estate)

### Timelock Policies

- Death Trigger Policy (Main Bitcoin Estate, ~10 days)
- Inactivity Policy (Main Bitcoin Estate, ~90 days)
- Manual Release (Family Trust Estate, 0 blocks)

## Resetting Demo Data

To reset and re-seed:

1. Delete existing demo user and related data from database
2. Run the script again

Or manually:

```sql
-- WARNING: This will delete all demo data
DELETE FROM timelock_policies WHERE estate_plan_id IN (
    SELECT id FROM estate_plans WHERE user_id IN (
        SELECT id FROM users WHERE email = 'demo@example.com'
    )
);
DELETE FROM beneficiaries WHERE estate_plan_id IN (
    SELECT id FROM estate_plans WHERE user_id IN (
        SELECT id FROM users WHERE email = 'demo@example.com'
    )
);
DELETE FROM estate_plans WHERE user_id IN (
    SELECT id FROM users WHERE email = 'demo@example.com'
);
DELETE FROM users WHERE email = 'demo@example.com';
```

Then run the seed script again.

## Notes

- The script is idempotent for the demo user (won't create duplicates)
- Estate plans, beneficiaries, and policies are always created fresh
- Bitcoin addresses are testnet addresses for safety
- Allocations total 100% per estate plan

