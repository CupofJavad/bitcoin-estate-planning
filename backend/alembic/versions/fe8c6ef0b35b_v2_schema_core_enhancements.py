"""v2_schema_core_enhancements

Revision ID: fe8c6ef0b35b
Revises: fc25d1181863
Create Date: 2025-12-29 02:08:55.965249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'fe8c6ef0b35b'
down_revision: Union[str, None] = 'fc25d1181863'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUM types (only if they don't exist)
    op.execute("DO $$ BEGIN CREATE TYPE partytype AS ENUM ('PERSON', 'ORGANIZATION'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE partystatus AS ENUM ('ACTIVE', 'INACTIVE', 'DECEASED', 'DISSOLVED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE roletype AS ENUM ('CLIENT', 'BENEFICIARY', 'EXECUTOR', 'ATTORNEY', 'ADVISOR', 'STAFF', 'ORACLE_PROVIDER', 'INSURANCE_UNDERWRITER', 'EXCHANGE_PARTNER', 'CUSTODY_PARTNER'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE contacttype AS ENUM ('EMAIL', 'PHONE', 'ADDRESS', 'SOCIAL', 'OTHER'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE accountstatus AS ENUM ('ACTIVE', 'LOCKED', 'DISABLED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE credentialtype AS ENUM ('PASSWORD', 'TOTP', 'FIDO2_PASSKEY', 'RECOVERY_CODE'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE devicetype AS ENUM ('MOBILE', 'DESKTOP', 'HARDWARE_WALLET', 'UNKNOWN'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE estateplanstatus AS ENUM ('DRAFT', 'ACTIVE', 'SUSPENDED', 'COMPLETED', 'CANCELLED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE estateplantype AS ENUM ('BITCOIN_ONLY', 'MULTI_ASSET', 'CHARITABLE', 'BUSINESS_SUCCESSION', 'CUSTOM'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE primarycurrency AS ENUM ('USD', 'EUR', 'BTC', 'GBP', 'CAD', 'AUD'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE versionstatus AS ENUM ('CURRENT', 'SUPERSEDED', 'REVOKED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE participantrole AS ENUM ('CLIENT', 'PRIMARY_BENEFICIARY', 'CONTINGENT_BENEFICIARY', 'EXECUTOR', 'CO_EXECUTOR', 'ATTORNEY_OF_RECORD', 'ADVISOR'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE allocationtype AS ENUM ('PERCENTAGE', 'FIXED_AMOUNT', 'TIERED', 'CONDITIONAL'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE inheritancestyle AS ENUM ('LUMP_SUM', 'ANNUITY', 'TRANCHE', 'TRUST_LIKE_STREAM'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE documenttype AS ENUM ('WILL', 'TRUST', 'ESTATE_ADDENDUM', 'LETTER_OF_WISHES', 'POWER_OF_ATTORNEY', 'INSURANCE_POLICY', 'OTHER'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE lifeeventtype AS ENUM ('MARRIAGE', 'DIVORCE', 'CHILD_BIRTH', 'ADOPTION', 'DEATH', 'INCAPACITY', 'MOVE_JURISDICTION', 'BUSINESS_SALE', 'MAJOR_ASSET_CHANGE', 'OTHER'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE kyccasestatus AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'REVIEW_REQUIRED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE risklevel AS ENUM ('LOW', 'MEDIUM', 'HIGH'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE kycdocumenttype AS ENUM ('PASSPORT', 'ID_CARD', 'DRIVER_LICENSE', 'UTILITY_BILL', 'BANK_STATEMENT', 'OTHER'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE screeningresult AS ENUM ('NO_MATCH', 'POTENTIAL_MATCH', 'CONFIRMED_MATCH'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE overallrisklevel AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE assessedby AS ENUM ('AI', 'HUMAN', 'MIXED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE wallettype AS ENUM ('MULTISIG_POLICY', 'SINGLE_SIG', 'MPC_MANAGED', 'EXTERNAL_DESCRIPTOR'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE walletstatus AS ENUM ('ACTIVE', 'ARCHIVED', 'COMPROMISED', 'DEPRECATED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE policylanguage AS ENUM ('MINISCRIPT', 'POLICY', 'CUSTOM_SCRIPT', 'EVM_CONTRACT', 'OTHER'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE policyversionstatus AS ENUM ('CURRENT', 'SUPERSEDED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE locktype AS ENUM ('ABSOLUTE', 'RELATIVE'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE actortype AS ENUM ('STAFF', 'CLIENT', 'BENEFICIARY', 'SYSTEM', 'AI'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE criticality AS ENUM ('INFO', 'WARNING', 'CRITICAL'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE deliverychannel AS ENUM ('EMAIL', 'SMS', 'APP_PUSH', 'PHONE_CALL', 'IN_APP'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE deliverystatus AS ENUM ('PENDING', 'SENT', 'FAILED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")

    # Party & Identity System
    # Check if table exists before creating
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'parties')"))
    if not result.scalar():
        op.create_table('parties',
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('party_type', postgresql.ENUM('PERSON', 'ORGANIZATION', name='partytype', create_type=False), nullable=False),
        sa.Column('legal_name', sa.String(length=500), nullable=False),
        sa.Column('preferred_name', sa.String(length=500), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('date_of_incorporation', sa.Date(), nullable=True),
        sa.Column('tax_id', sa.String(length=100), nullable=True),
        sa.Column('primary_residence_country', sa.String(length=2), nullable=True),
        sa.Column('primary_residence_region', sa.String(length=100), nullable=True),
        sa.Column('primary_residence_city', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('status', postgresql.ENUM('ACTIVE', 'INACTIVE', 'DECEASED', 'DISSOLVED', name='partystatus', create_type=False), nullable=False),
        sa.PrimaryKeyConstraint('party_id')
        )
        op.create_index(op.f('ix_parties_party_id'), 'parties', ['party_id'], unique=False)

    result = conn.execute(sa.text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'party_roles')"))
    if not result.scalar():
        op.create_table('party_roles',
        sa.Column('party_role_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role_type', postgresql.ENUM('CLIENT', 'BENEFICIARY', 'EXECUTOR', 'ATTORNEY', 'ADVISOR', 'STAFF', 'ORACLE_PROVIDER', 'INSURANCE_UNDERWRITER', 'EXCHANGE_PARTNER', 'CUSTODY_PARTNER', name='roletype', create_type=False), nullable=False),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('party_role_id')
    )

    op.create_table('contact_info',
        sa.Column('contact_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('contact_type', postgresql.ENUM('EMAIL', 'PHONE', 'ADDRESS', 'SOCIAL', 'OTHER', name='contacttype', create_type=False), nullable=False),
        sa.Column('value', sa.String(length=500), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('contact_id')
    )

    op.create_table('accounts',
        sa.Column('account_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('status', postgresql.ENUM('ACTIVE', 'LOCKED', 'DISABLED', name='accountstatus', create_type=False), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('account_id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_accounts_username'), 'accounts', ['username'], unique=True)
    op.create_index(op.f('ix_accounts_email'), 'accounts', ['email'], unique=True)

    op.create_table('auth_credentials',
        sa.Column('auth_credential_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('account_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('credential_type', postgresql.ENUM('PASSWORD', 'TOTP', 'FIDO2_PASSKEY', 'RECOVERY_CODE', name='credentialtype', create_type=False), nullable=False),
        sa.Column('public_key', sa.String(length=1000), nullable=True),
        sa.Column('config_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.account_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('auth_credential_id')
    )

    op.create_table('devices',
        sa.Column('device_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('device_fingerprint', sa.String(length=255), nullable=False),
        sa.Column('device_type', postgresql.ENUM('MOBILE', 'DESKTOP', 'HARDWARE_WALLET', 'UNKNOWN', name='devicetype', create_type=False), nullable=False),
        sa.Column('os', sa.String(length=100), nullable=True),
        sa.Column('last_seen_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('trusted', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('device_id')
    )
    op.create_index(op.f('ix_devices_device_fingerprint'), 'devices', ['device_fingerprint'], unique=False)

    # Jurisdictions
    op.create_table('jurisdictions',
        sa.Column('jurisdiction_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('country_code', sa.String(length=2), nullable=False),
        sa.Column('region_code', sa.String(length=10), nullable=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('estate_tax_rules_ref', sa.Text(), nullable=True),
        sa.Column('inheritance_law_notes', sa.Text(), nullable=True),
        sa.Column('crypto_regulation_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('jurisdiction_id')
    )
    op.create_index(op.f('ix_jurisdictions_country_code'), 'jurisdictions', ['country_code'], unique=False)
    op.create_index(op.f('ix_jurisdictions_region_code'), 'jurisdictions', ['region_code'], unique=False)

    # Enhanced Estate Planning
    op.create_table('estate_plans_v2',
        sa.Column('estate_plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('client_party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('primary_executor_party_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('plan_status', postgresql.ENUM('DRAFT', 'ACTIVE', 'SUSPENDED', 'COMPLETED', 'CANCELLED', name='estateplanstatus', create_type=False), nullable=False),
        sa.Column('plan_type', postgresql.ENUM('BITCOIN_ONLY', 'MULTI_ASSET', 'CHARITABLE', 'BUSINESS_SUCCESSION', 'CUSTOM', name='estateplantype', create_type=False), nullable=False),
        sa.Column('governing_jurisdiction_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('primary_currency', postgresql.ENUM('USD', 'EUR', 'BTC', 'GBP', 'CAD', 'AUD', name='primarycurrency', create_type=False), nullable=False),
        sa.Column('effective_date', sa.Date(), nullable=True),
        sa.Column('termination_date', sa.Date(), nullable=True),
        sa.Column('review_frequency_months', sa.Integer(), nullable=False),
        sa.Column('next_review_due_at', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['client_party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['primary_executor_party_id'], ['parties.party_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['governing_jurisdiction_id'], ['jurisdictions.jurisdiction_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('estate_plan_id')
    )

    op.create_table('estate_plan_versions',
        sa.Column('estate_plan_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('estate_plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('status', postgresql.ENUM('CURRENT', 'SUPERSEDED', 'REVOKED', name='versionstatus', create_type=False), nullable=False),
        sa.Column('approved_by_party_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('effective_from', sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_to', sa.DateTime(timezone=True), nullable=True),
        sa.Column('snapshot_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['estate_plan_id'], ['estate_plans_v2.estate_plan_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['approved_by_party_id'], ['parties.party_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('estate_plan_version_id')
    )

    op.create_table('estate_plan_participants',
        sa.Column('estate_plan_participant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('estate_plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', postgresql.ENUM('CLIENT', 'PRIMARY_BENEFICIARY', 'CONTINGENT_BENEFICIARY', 'EXECUTOR', 'CO_EXECUTOR', 'ATTORNEY_OF_RECORD', 'ADVISOR', name='participantrole', create_type=False), nullable=False),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['estate_plan_id'], ['estate_plans_v2.estate_plan_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('estate_plan_participant_id')
    )

    op.create_table('beneficiary_allocations',
        sa.Column('beneficiary_allocation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('estate_plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('beneficiary_party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('allocation_type', postgresql.ENUM('PERCENTAGE', 'FIXED_AMOUNT', 'TIERED', 'CONDITIONAL', name='allocationtype', create_type=False), nullable=False),
        sa.Column('allocation_value', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('priority_order', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('conditions_ref', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('inheritance_style', postgresql.ENUM('LUMP_SUM', 'ANNUITY', 'TRANCHE', 'TRUST_LIKE_STREAM', name='inheritancestyle', create_type=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['estate_plan_id'], ['estate_plans_v2.estate_plan_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['beneficiary_party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('beneficiary_allocation_id')
    )

    op.create_table('legal_documents',
        sa.Column('legal_document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('estate_plan_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('document_type', postgresql.ENUM('WILL', 'TRUST', 'ESTATE_ADDENDUM', 'LETTER_OF_WISHES', 'POWER_OF_ATTORNEY', 'INSURANCE_POLICY', 'OTHER', name='documenttype', create_type=False), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('storage_location', sa.String(length=1000), nullable=False),
        sa.Column('hash', sa.String(length=128), nullable=False),
        sa.Column('signed_date', sa.Date(), nullable=True),
        sa.Column('effective_from', sa.Date(), nullable=True),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['estate_plan_id'], ['estate_plans_v2.estate_plan_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('legal_document_id')
    )

    op.create_table('life_events',
        sa.Column('life_event_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('estate_plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', postgresql.ENUM('MARRIAGE', 'DIVORCE', 'CHILD_BIRTH', 'ADOPTION', 'DEATH', 'INCAPACITY', 'MOVE_JURISDICTION', 'BUSINESS_SALE', 'MAJOR_ASSET_CHANGE', 'OTHER', name='lifeeventtype', create_type=False), nullable=False),
        sa.Column('subject_party_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('event_date', sa.Date(), nullable=False),
        sa.Column('evidence_ref', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('recorded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('recorded_by_party_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['estate_plan_id'], ['estate_plans_v2.estate_plan_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_party_id'], ['parties.party_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['recorded_by_party_id'], ['parties.party_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('life_event_id')
    )

    # Compliance
    op.create_table('kyc_cases',
        sa.Column('kyc_case_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', 'REVIEW_REQUIRED', name='kyccasestatus', create_type=False), nullable=False),
        sa.Column('risk_level', postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', name='risklevel', create_type=False), nullable=True),
        sa.Column('provider', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('kyc_case_id')
    )

    op.create_table('kyc_documents',
        sa.Column('kyc_document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('kyc_case_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_type', postgresql.ENUM('PASSPORT', 'ID_CARD', 'DRIVER_LICENSE', 'UTILITY_BILL', 'BANK_STATEMENT', 'OTHER', name='kycdocumenttype', create_type=False), nullable=False),
        sa.Column('storage_location', sa.String(length=1000), nullable=False),
        sa.Column('hash', sa.String(length=128), nullable=False),
        sa.Column('issue_country', sa.String(length=2), nullable=True),
        sa.Column('issue_date', sa.Date(), nullable=True),
        sa.Column('expiry_date', sa.Date(), nullable=True),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['kyc_case_id'], ['kyc_cases.kyc_case_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('kyc_document_id')
    )

    op.create_table('sanctions_screenings',
        sa.Column('sanctions_screening_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('kyc_case_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('screening_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('result', postgresql.ENUM('NO_MATCH', 'POTENTIAL_MATCH', 'CONFIRMED_MATCH', name='screeningresult', create_type=False), nullable=False),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['kyc_case_id'], ['kyc_cases.kyc_case_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('sanctions_screening_id')
    )

    op.create_table('party_risk_profiles',
        sa.Column('party_risk_profile_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('overall_risk_level', postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', name='overallrisklevel', create_type=False), nullable=False),
        sa.Column('risk_factors', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('last_assessed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('assessed_by', postgresql.ENUM('AI', 'HUMAN', 'MIXED', name='assessedby', create_type=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('party_risk_profile_id'),
        sa.UniqueConstraint('party_id')
    )

    # Wallet & Policies
    op.create_table('networks',
        sa.Column('network_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('network_type', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('rpc_endpoint_ref', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('chain_id', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('network_id')
    )

    op.create_table('wallets',
        sa.Column('wallet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('estate_plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('network_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('wallet_name', sa.String(length=255), nullable=False),
        sa.Column('wallet_type', postgresql.ENUM('MULTISIG_POLICY', 'SINGLE_SIG', 'MPC_MANAGED', 'EXTERNAL_DESCRIPTOR', name='wallettype', create_type=False), nullable=False),
        sa.Column('descriptor', sa.String(length=2000), nullable=True),
        sa.Column('is_inheritance_wallet', sa.Boolean(), nullable=False),
        sa.Column('status', postgresql.ENUM('ACTIVE', 'ARCHIVED', 'COMPROMISED', 'DEPRECATED', name='walletstatus', create_type=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['estate_plan_id'], ['estate_plans_v2.estate_plan_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['network_id'], ['networks.network_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('wallet_id')
    )

    op.create_table('script_templates',
        sa.Column('script_template_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('policy_language', sa.String(length=50), nullable=False),
        sa.Column('policy_template_text', sa.Text(), nullable=False),
        sa.Column('default_parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('supports_pqc', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('script_template_id')
    )

    op.create_table('wallet_policy_versions',
        sa.Column('wallet_policy_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('wallet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('status', postgresql.ENUM('CURRENT', 'SUPERSEDED', name='policyversionstatus', create_type=False), nullable=False),
        sa.Column('policy_language', postgresql.ENUM('MINISCRIPT', 'POLICY', 'CUSTOM_SCRIPT', 'EVM_CONTRACT', 'OTHER', name='policylanguage', create_type=False), nullable=False),
        sa.Column('policy_text', sa.Text(), nullable=True),
        sa.Column('script_template_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('effective_from', sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_to', sa.DateTime(timezone=True), nullable=True),
        sa.Column('upgrade_reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['wallet_id'], ['wallets.wallet_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['script_template_id'], ['script_templates.script_template_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('wallet_policy_version_id')
    )

    op.create_table('timelock_configs',
        sa.Column('timelock_config_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('wallet_policy_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('lock_type', postgresql.ENUM('ABSOLUTE', 'RELATIVE', name='locktype', create_type=False), nullable=False),
        sa.Column('absolute_block_height', sa.BigInteger(), nullable=True),
        sa.Column('absolute_timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.Column('relative_blocks', sa.BigInteger(), nullable=True),
        sa.Column('relative_days', sa.Integer(), nullable=True),
        sa.Column('primary_path_delay_days', sa.Integer(), nullable=True),
        sa.Column('heir_path_delay_days', sa.Integer(), nullable=True),
        sa.Column('backup_path_delay_days', sa.Integer(), nullable=True),
        sa.Column('refresh_threshold_days', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['wallet_policy_version_id'], ['wallet_policy_versions.wallet_policy_version_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('timelock_config_id')
    )

    # Audit & Notifications
    op.create_table('audit_logs',
        sa.Column('audit_log_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('actor_type', postgresql.ENUM('STAFF', 'CLIENT', 'BENEFICIARY', 'SYSTEM', 'AI', name='actortype', create_type=False), nullable=False),
        sa.Column('actor_party_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('actor_account_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('entity_type', sa.String(length=100), nullable=True),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('ip_address', postgresql.INET(), nullable=True),
        sa.Column('device_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('criticality', postgresql.ENUM('INFO', 'WARNING', 'CRITICAL', name='criticality', create_type=False), nullable=False),
        sa.ForeignKeyConstraint(['actor_party_id'], ['parties.party_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['actor_account_id'], ['accounts.account_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['device_id'], ['devices.device_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('audit_log_id')
    )
    op.create_index(op.f('ix_audit_logs_timestamp'), 'audit_logs', ['timestamp'], unique=False)
    op.create_index(op.f('ix_audit_logs_event_type'), 'audit_logs', ['event_type'], unique=False)

    op.create_table('notification_preferences',
        sa.Column('notification_preference_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('channel', postgresql.ENUM('EMAIL', 'SMS', 'APP_PUSH', 'PHONE_CALL', 'IN_APP', name='deliverychannel', create_type=False), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('enabled', sa.String(length=10), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('notification_preference_id')
    )

    op.create_table('notifications',
        sa.Column('notification_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('recipient_party_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('delivery_channel', postgresql.ENUM('EMAIL', 'SMS', 'APP_PUSH', 'PHONE_CALL', 'IN_APP', name='deliverychannel', create_type=False), nullable=False),
        sa.Column('delivery_status', postgresql.ENUM('PENDING', 'SENT', 'FAILED', name='deliverystatus', create_type=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['recipient_party_id'], ['parties.party_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('notification_id')
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('notifications')
    op.drop_table('notification_preferences')
    op.drop_table('audit_logs')
    op.drop_table('timelock_configs')
    op.drop_table('wallet_policy_versions')
    op.drop_table('script_templates')
    op.drop_table('wallets')
    op.drop_table('networks')
    op.drop_table('party_risk_profiles')
    op.drop_table('sanctions_screenings')
    op.drop_table('kyc_documents')
    op.drop_table('kyc_cases')
    op.drop_table('life_events')
    op.drop_table('legal_documents')
    op.drop_table('beneficiary_allocations')
    op.drop_table('estate_plan_participants')
    op.drop_table('estate_plan_versions')
    op.drop_table('estate_plans_v2')
    op.drop_table('jurisdictions')
    op.drop_table('devices')
    op.drop_table('auth_credentials')
    op.drop_table('accounts')
    op.drop_table('contact_info')
    op.drop_table('party_roles')
    op.drop_table('parties')

    # Drop ENUM types
    op.execute("DROP TYPE IF EXISTS deliverystatus")
    op.execute("DROP TYPE IF EXISTS deliverychannel")
    op.execute("DROP TYPE IF EXISTS criticality")
    op.execute("DROP TYPE IF EXISTS actortype")
    op.execute("DROP TYPE IF EXISTS locktype")
    op.execute("DROP TYPE IF EXISTS policyversionstatus")
    op.execute("DROP TYPE IF EXISTS policylanguage")
    op.execute("DROP TYPE IF EXISTS walletstatus")
    op.execute("DROP TYPE IF EXISTS wallettype")
    op.execute("DROP TYPE IF EXISTS assessedby")
    op.execute("DROP TYPE IF EXISTS overallrisklevel")
    op.execute("DROP TYPE IF EXISTS screeningresult")
    op.execute("DROP TYPE IF EXISTS kycdocumenttype")
    op.execute("DROP TYPE IF EXISTS risklevel")
    op.execute("DROP TYPE IF EXISTS kyccasestatus")
    op.execute("DROP TYPE IF EXISTS lifeeventtype")
    op.execute("DROP TYPE IF EXISTS documenttype")
    op.execute("DROP TYPE IF EXISTS inheritancestyle")
    op.execute("DROP TYPE IF EXISTS allocationtype")
    op.execute("DROP TYPE IF EXISTS participantrole")
    op.execute("DROP TYPE IF EXISTS versionstatus")
    op.execute("DROP TYPE IF EXISTS primarycurrency")
    op.execute("DROP TYPE IF EXISTS estateplantype")
    op.execute("DROP TYPE IF EXISTS estateplanstatus")
    op.execute("DROP TYPE IF EXISTS devicetype")
    op.execute("DROP TYPE IF EXISTS credentialtype")
    op.execute("DROP TYPE IF EXISTS accountstatus")
    op.execute("DROP TYPE IF EXISTS contacttype")
    op.execute("DROP TYPE IF EXISTS roletype")
    op.execute("DROP TYPE IF EXISTS partystatus")
    op.execute("DROP TYPE IF EXISTS partytype")
