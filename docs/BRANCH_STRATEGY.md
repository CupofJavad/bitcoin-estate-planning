# Branch Strategy & Version Management

## Current State

**Version:** 1.01  
**Tag:** `v1.01`  
**Branch:** `feature/investor-demo-v1`  
**Status:** ✅ Stable - Investor Demo Ready

## Version Tagging

Version 1.01 has been tagged to preserve the current state:

```bash
git tag -a v1.01 -m "Version 1.01 - Investor Demo Ready"
```

This tag preserves:
- Complete UI with all CRUD operations
- Estate Plans, Beneficiaries, and Timelock Policies management
- Professional investor-ready interface
- Comprehensive testing documentation
- All frontend-backend connections verified

## Branch Strategy

### Main Branches

#### `main` Branch
- **Purpose**: Production-ready, stable code
- **Protection**: Should be protected, requires PR review
- **Merges**: Only from `develop` or `release/*` branches
- **Tags**: Major version releases (v1.0, v2.0, etc.)

#### `develop` Branch
- **Purpose**: Integration branch for features
- **Merges**: Feature branches merge here
- **Status**: Always deployable to staging
- **Tags**: Minor version releases (v1.1, v1.2, etc.)

### Feature Branches

#### Naming Convention
- `feature/feature-name` - New features
- `feature/investor-demo-v1` - Current branch (v1.01)

#### Workflow
1. Create from `develop` or `main`
2. Develop feature
3. Test thoroughly
4. Create PR to `develop`
5. Merge after review
6. Delete branch after merge

### Bugfix Branches

#### Naming Convention
- `bugfix/issue-description` - Bug fixes

#### Workflow
1. Create from `develop` or `main`
2. Fix bug
3. Add tests
4. Create PR
5. Merge after review

### Hotfix Branches

#### Naming Convention
- `hotfix/critical-issue` - Critical production fixes

#### Workflow
1. Create from `main`
2. Fix critical issue
3. Test thoroughly
4. Merge to both `main` and `develop`
5. Tag new version immediately

### Release Branches

#### Naming Convention
- `release/v1.02` - Release preparation

#### Workflow
1. Create from `develop` when ready for release
2. Final testing and bug fixes
3. Update version numbers
4. Merge to `main` and tag version
5. Merge back to `develop`

## Version Numbering

### Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Current Versions

- **v1.01**: Investor Demo Ready (current)
- Future: v1.02, v1.03, v2.0.0, etc.

## Workflow Examples

### Starting a New Feature

```bash
# Ensure you're on develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/authentication

# Develop and commit
git add .
git commit -m "feat: add user authentication"

# Push branch
git push origin feature/authentication

# Create PR on GitHub
```

### Creating a Release

```bash
# Create release branch
git checkout -b release/v1.02 develop

# Final testing and fixes
# Update version numbers
# Update CHANGELOG.md

# Merge to main
git checkout main
git merge release/v1.02

# Tag version
git tag -a v1.02 -m "Version 1.02 - New features"
git push origin v1.02

# Merge back to develop
git checkout develop
git merge release/v1.02

# Delete release branch
git branch -d release/v1.02
```

### Hotfix Workflow

```bash
# Create hotfix from main
git checkout main
git checkout -b hotfix/critical-bug

# Fix bug
git add .
git commit -m "fix: critical security issue"

# Merge to main
git checkout main
git merge hotfix/critical-bug
git tag -a v1.01.1 -m "Hotfix: critical security issue"
git push origin v1.01.1

# Merge to develop
git checkout develop
git merge hotfix/critical-bug

# Delete hotfix branch
git branch -d hotfix/critical-bug
```

## Preserving Current State (v1.01)

The current state is preserved via:

1. **Git Tag**: `v1.01` - Immutable reference point
2. **Branch**: `feature/investor-demo-v1` - Development branch
3. **Documentation**: All features documented in README.md

### To Restore v1.01

```bash
# Checkout the tagged version
git checkout v1.01

# Or create a branch from the tag
git checkout -b restore-v1.01 v1.01
```

### To Continue Development

```bash
# Stay on current branch or create new feature branch
git checkout feature/investor-demo-v1
# or
git checkout -b feature/new-feature
```

## Best Practices

1. **Always create feature branches** - Never commit directly to `main` or `develop`
2. **Write descriptive commit messages** - Follow conventional commits format
3. **Test before merging** - Ensure all tests pass
4. **Update documentation** - Keep README and docs current
5. **Tag releases** - Tag all significant versions
6. **Delete merged branches** - Keep repository clean

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(estate-plans): add search functionality
fix(beneficiaries): prevent allocation > 100%
docs(readme): update installation instructions
test(api): add integration tests for estate plans
```

## Branch Protection Rules

Recommended for `main` and `develop`:

1. Require pull request reviews
2. Require status checks to pass
3. Require branches to be up to date
4. Require linear history (no merge commits)
5. Do not allow force pushes
6. Do not allow deletions

---

## Summary

- ✅ **v1.01 tagged** - Current state preserved
- ✅ **Branch strategy** - Documented and ready
- ✅ **Future changes** - Will occur on new branches
- ✅ **Version management** - Semantic versioning
- ✅ **Workflow** - Clear processes for all scenarios

