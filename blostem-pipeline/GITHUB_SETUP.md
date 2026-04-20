# GitHub Setup Instructions

## Step 1: Initialize Git Repository

```bash
cd blostem-pipeline
git init
git add .
git commit -m "Initial commit: Blostem Pipeline - B2B Marketing Automation Engine"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `blostem-pipeline`
3. Do NOT initialize with README, .gitignore, or license (we already have them)
4. Click "Create repository"

## Step 3: Add Remote and Push

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/blostem-pipeline.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Verify

Visit `https://github.com/YOUR_USERNAME/blostem-pipeline` to verify the repository is live.

## Step 5: Add Repository Description

On GitHub:
1. Go to repository settings
2. Add description: "AI-powered B2B marketing automation engine for fintech"
3. Add topics: `fintech`, `marketing-automation`, `fastapi`, `react`, `langchain`
4. Enable "Discussions" if desired

## Step 6: Create Releases

```bash
# Create a tag for version 1.0.0
git tag -a v1.0.0 -m "Initial release - Blostem Pipeline v1.0.0"

# Push tags to GitHub
git push origin v1.0.0
```

Then on GitHub:
1. Go to "Releases"
2. Click "Create a release"
3. Select tag `v1.0.0`
4. Add release notes describing features

## Step 7: Enable GitHub Actions

The `.github/workflows/test.yml` file will automatically run tests on push and pull requests.

## Step 8: Add Collaborators (Optional)

1. Go to repository Settings → Collaborators
2. Add team members who should have access

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create a new branch for features
git checkout -b feature/new-feature

# Push branch to GitHub
git push -u origin feature/new-feature

# Create a pull request on GitHub for the branch
# Then merge after review
```

## .gitignore Verification

The `.gitignore` file already excludes:
- `.env` files (API keys)
- `__pycache__/` (Python cache)
- `node_modules/` (npm packages)
- `*.db` (SQLite databases)
- `.vscode/` and `.idea/` (IDE files)
- Build artifacts

## Important Notes

1. **Never commit `.env` files** — Always use `.env.example`
2. **Never commit `node_modules/`** — Users run `npm install`
3. **Never commit `__pycache__/`** — Python cache is auto-generated
4. **Never commit `*.db` files** — Database is seeded with `python seed.py`

## Updating Repository

```bash
# Make changes
git add .
git commit -m "feat: add new feature"
git push origin main
```

## Creating Releases

```bash
# Tag a release
git tag -a v1.1.0 -m "Version 1.1.0 - Added email sending"
git push origin v1.1.0

# Then create release on GitHub with release notes
```

---

Your repository is now ready for GitHub! 🚀
