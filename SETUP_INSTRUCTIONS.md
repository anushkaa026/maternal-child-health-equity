# Setup Instructions

Follow these steps **exactly** to get your project set up!

## Step 1: Download the Project Files

Download the `maternal-child-health-equity` folder I've created and move it to your Desktop.

## Step 2: Open Terminal

Open your Terminal app (Command + Space, type "Terminal")

## Step 3: Navigate to the Project

```bash
cd ~/Desktop/maternal-child-health-equity
pwd
```

You should see: `/Users/anushkaanand/Desktop/maternal-child-health-equity`

## Step 4: Initialize Git

```bash
git init
git branch -M main
```

## Step 5: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your terminal should now show `(.venv)` at the beginning of the line.

## Step 6: Install Packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take a few minutes. Let it run!

## Step 7: Open in PyCharm

1. Open PyCharm
2. Click "Open"
3. Navigate to `Desktop/maternal-child-health-equity`
4. Click "Open"

## Step 8: Configure PyCharm Interpreter

1. In PyCharm, go to: **PyCharm → Settings** (or **Preferences** on Mac)
2. Navigate to: **Project: maternal-child-health-equity → Python Interpreter**
3. Click the **gear icon** → **Add Interpreter** → **Add Local Interpreter**
4. Select **"Existing"**
5. Navigate to: `/Users/anushkaanand/Desktop/maternal-child-health-equity/.venv/bin/python`
6. Click **"OK"**

## Step 9: Test Jupyter

In PyCharm's terminal (at the bottom):

```bash
jupyter notebook
```

This should open a browser window with Jupyter. Navigate to the `notebooks/` folder and open `01_data_exploration.ipynb`.

## Step 10: Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click the **"+"** → **"New repository"**
3. Name it: `maternal-child-health-equity`
4. Make it **Public**
5. **DO NOT** check "Initialize with README"
6. Click **"Create repository"**

## Step 11: Connect to GitHub

In your terminal:

```bash
git remote add origin https://github.com/anushkaa026/maternal-child-health-equity.git
git add .
git commit -m "Initial project structure and documentation"
git push -u origin main
```

If it asks for credentials, you'll need to create a **Personal Access Token**:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select "repo" scope
4. Use token as password when pushing

## Step 12: Start Working!

Open `notebooks/01_data_exploration.ipynb` in PyCharm and start running cells!

## Commit Strategy

After completing each notebook, commit your work:

```bash
git add notebooks/01_data_exploration.ipynb
git commit -m "Complete initial data exploration and summary statistics"
git push
```

After notebook 2:
```bash
git add notebooks/02_data_cleaning.ipynb data/processed/
git commit -m "Implement data cleaning pipeline and validation"
git push
```

Continue this pattern for each notebook!

## Troubleshooting

### "Python not found"
Make sure you're using `python3`, not `python`.

### "Permission denied"
Run: `chmod +x .venv/bin/activate`

### "Module not found"
Make sure your virtual environment is activated (you should see `.venv` in your terminal prompt).

### PyCharm can't find packages
Make sure you selected the correct Python interpreter (Step 8).

## Questions?

If you get stuck, check:
- Are you in the right directory? (`pwd` should show the project folder)
- Is your venv activated? (terminal should show `.venv`)
- Did all packages install? (check for errors in Step 6)
