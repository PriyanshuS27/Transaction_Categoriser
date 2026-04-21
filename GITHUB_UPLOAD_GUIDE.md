# GitHub Upload Instructions

Follow these steps to upload your Transaction Categorization project to GitHub:

## Step 1: Create a GitHub Account (if you don't have one)
- Go to https://github.com
- Sign up for a free account

## Step 2: Create a New Repository on GitHub

1. Log in to GitHub
2. Click the **+** icon in the top-right corner
3. Select **New repository**
4. Enter repository details:
   - **Repository name**: `transaction-categorizer` (or any name you prefer)
   - **Description**: "AI-powered transaction categorization service using Groq API"
   - **Public** (to make it public as requested)
   - **Add .gitignore**: Already created in project
   - **Add README**: Already created in project
5. Click **Create repository**

## Step 3: Initialize Git in Your Project

Open PowerShell and navigate to your project directory:

```powershell
cd "c:\Users\Admin\PythonProjects\App_Deft_Assignment\transaction_categorizer"
```

Initialize git repository:

```powershell
git init
```

Add all files:

```powershell
git add .
```

Create initial commit:

```powershell
git commit -m "Initial commit: Transaction categorization service with Groq API integration"
```

## Step 4: Connect to GitHub Repository

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

Example:
```powershell
git remote add origin https://github.com/priyanshu-sharma/transaction-categorizer.git
```

## Step 5: Push to GitHub

First, rename the branch to `main` (GitHub's default):

```powershell
git branch -M main
```

Push your code:

```powershell
git push -u origin main
```

If prompted for credentials, use your GitHub token:
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate a new token with `repo` scope
- Use the token as password when prompted

## Step 6: Verify Your Repository

1. Go to https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
2. Verify all files are uploaded
3. Check that README.md and requirements.txt are visible
4. Verify the repository is **Public**

---

## ✅ What Gets Uploaded:

```
✓ Source code (.py files)
✓ README.md (documentation)
✓ requirements.txt (dependencies)
✓ .gitignore (excludes venv, logs, .env)
✓ Configuration files
✓ Tests
✓ Documentation (IMPROVEMENTS.md)
```

## ❌ What Gets Ignored (Not Uploaded):

```
✗ venv/ (virtual environment)
✗ __pycache__/ (compiled Python files)
✗ .env (API keys - SECURITY!)
✗ db.sqlite3 (database)
✗ logs/ (log files)
```

---

## Optional: Add More Information to GitHub

### 1. Add Project Description
- Click **Settings** → **Repository details**
- Add description and topics (e.g., `django`, `groq`, `llm`, `ai`)

### 2. Add GitHub Actions (CI/CD)
Create `.github/workflows/tests.yml` for automated testing:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python test_suite.py
```

### 3. Add License
- Click **Add file** → **Create new file**
- Name it `LICENSE`
- Choose a license (MIT, Apache 2.0, etc.)

### 4. Add Badges to README
Add these to your README for visual appeal:

```markdown
[![Tests](https://github.com/YOUR_USERNAME/transaction-categorizer/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/transaction-categorizer/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

---

## Troubleshooting

### `fatal: not a git repository`
```powershell
git init
```

### `error: The current branch main has no upstream branch`
```powershell
git push -u origin main
```

### `Permission denied (publickey)`
- Go to GitHub → Settings → SSH and GPG keys
- Add your SSH key or use HTTPS with personal access token

### Want to Make Changes and Update?
```powershell
git add .
git commit -m "Update: description of changes"
git push
```

---

## Final Checklist

✅ Repository created on GitHub  
✅ Git initialized locally  
✅ Files committed  
✅ Remote added  
✅ Code pushed to main  
✅ Repository is PUBLIC  
✅ README.md visible  
✅ requirements.txt visible  

---

## Your Repository URL

Once uploaded, your repository will be at:

```
https://github.com/YOUR_USERNAME/transaction-categorizer
```

Share this link with HR/Team! 🚀
