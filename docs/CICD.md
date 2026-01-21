# CI/CD & Workflows Guide

Comprehensive guide for GitHub Actions workflows and continuous integration.

## Workflows Overview

The framework includes **4 automated workflows** for different testing scenarios:

### 1. E2E Tests (`e2e-tests.yml`)

**Purpose:** Full E2E test suite with multi-browser support  
**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Manual dispatch
- Scheduled runs

**Features:**
- Multi-browser: Chromium, Firefox, WebKit
- Allure report generation with history
- VPS deployment for reports
- Video/screenshot/trace on failure
- Manual test selection

**Manual Trigger:**
```bash
gh workflow run e2e-tests.yml -f app=sauce_demo -f browser=chromium
```

---

### 2. API Tests (`api-tests.yml`)

**Purpose:** Fast API testing with parallel execution  
**Triggers:**
- Push to `main` or `develop`
- Pull requests
- Manual dispatch

**Features:**
- Parallel execution (`-n auto`)
- Fast feedback (~2-3 min)
- Per-app test selection
- Allure reporting
- GitHub Actions summary with test counts

**Run Specific API:**
```bash
gh workflow run api-tests.yml -f app=reqres
```

**Supported Apps:** `restful_booker`, `petstore`, `omdb`, `reqres`

---

### 3. Smoke Tests (`smoke-tests.yml`)

**Purpose:** Quick validation of critical paths  
**Triggers:**
- Every pull request
- Push to `main/develop`

**Features:**
- Fastest execution (~5-10 min)
- Critical path validation only
- Automatic PR comments with results
- Parallel execution
- No artifacts (speed focused)

**How to Mark Smoke Tests:**
```python
@pytest.mark.smoke
def test_critical_login():
    """Critical path test"""
    pass
```

---

### 4. Nightly Regression (`nightly-regression.yml`)

**Purpose:** Complete regression suite  
**Triggers:**
- Daily at 2 AM UTC
- Manual dispatch

**Features:**
- Full test suite (E2E + API)
- Matrix strategy for parallelization
- 7-day report retention
- Comprehensive quality checks

**Execution Time:** ~30-40 minutes

---

## GitHub Secrets Configuration

### Required Secrets

Navigate to **Settings → Secrets and variables → Actions** and add:

```
OMDB_API_KEY          # Required for OMDb API tests
```

### Optional Secrets (VPS Deployment)

```
VPS_SSH_KEY           # SSH private key for deployment
VPS_HOST              # VPS hostname/IP
VPS_USER              # VPS username
VPS_DEPLOY_PATH       # Report deployment path
```

**Generate SSH Key:**
```bash
ssh-keygen -t ed25519 -C "github-actions"
# Add public key to VPS: ~/.ssh/authorized_keys
# Copy private key to GitHub secret: VPS_SSH_KEY
```

---

## Workflow Status Badges

Add to your README:

```markdown
[![E2E Tests](https://github.com/username/repo/workflows/E2E%20Tests/badge.svg)](https://github.com/username/repo/actions)
[![API Tests](https://github.com/username/repo/workflows/API%20Tests/badge.svg)](https://github.com/username/repo/actions)
[![Smoke Tests](https://github.com/username/repo/workflows/Smoke%20Tests/badge.svg)](https://github.com/username/repo/actions)
```

Replace `username/repo` with your repository path.

---

## Local Testing with CI Configuration

**Test E2E workflow locally:**
```bash
pytest apps/e2e/ \
  --browser chromium \
  --alluredir=test-results/allure-results \
  --video=retain-on-failure \
  --screenshot=only-on-failure
```

**Test API workflow locally:**
```bash
pytest apps/api/ -v -n auto --alluredir=test-results/allure-results
```

**Test smoke suite:**
```bash
pytest -m smoke -v -n auto --tb=short
```

---

##  Viewing Reports

### Local Allure Reports

```bash
# Generate and open
make report

# Or manually
allure generate test-results/allure-results --clean -o test-results/allure-report
allure open test-results/allure-report
```

### CI Allure Reports

1. Go to **Actions** tab in GitHub
2. Select workflow run
3. Download `allure-report` artifact
4. Extract and open `index.html`

**VPS Deployment (if configured):**
Reports automatically deployed to `https://your-domain.com/latest/allure-report/`

---

## Parallel Execution

**Local:**
```bash
make test-parallel  # Uses all CPU cores
pytest -n 4         # Use 4 workers
pytest -n auto      # Auto-detect cores
```

**CI:** Already configured in workflows (`-n auto`)

---

## Troubleshooting

### Workflow Fails: "Allure not found"

Allure is installed automatically in CI. Verify `.github/workflows/*.yml` has:
```yaml
- name: Install Allure
  run: |
    wget -q https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.tgz
    tar -xzf allure-2.25.0.tgz
    echo "$PWD/allure-2.25.0/bin" >> $GITHUB_PATH
```

### Workflow Fails: "Playwright not installed"

Check workflow includes:
```yaml
- name: Install Playwright browsers
  run: |
    playwright install chromium --with-deps
```

### Tests Pass Locally But Fail in CI

Common causes:
- Missing environment variables/secrets
- Different Python/dependency versions
- Timing issues (increase timeouts in CI)

**Debug with:**
```yaml
- name: Debug environment
  run: |
    python --version
    pip list
    playwright --version
```

---

## Best Practices

✅ **DO:**
- Tag smoke tests with `@pytest.mark.smoke`
- Keep smoke tests fast (<10 min total)
- Use parallel execution for API tests
- Review Allure reports after failures

❌ **DON'T:**
- Run full E2E suite on every PR (use smoke tests)
- Skip test isolation (each test should be independent)
- Hard-code secrets in workflows

---

**See also:**
- [Testing Guide](TESTING.md) - Detailed test execution
- [Setup Guide](SETUP.md) - Installation instructions
