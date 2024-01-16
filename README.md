
# Getting Started with GitHub Actions

GitHub Actions is a powerful automation feature provided by GitHub that allows you to build, test, and deploy your code directly from your repository. It helps automate various workflows, making your development process more efficient.

## What is GitHub Actions?

GitHub Actions is a CI/CD (Continuous Integration/Continuous Deployment) service provided by GitHub. It enables you to automate tasks such as building and testing your code, running scripts, and deploying applications. With GitHub Actions, you can define custom workflows using YAML files directly in your repository.

## How to Use GitHub Actions

### 1. Creating Workflow Files

To get started, create a `.github/workflows` directory in your repository. Inside this directory, you can add YAML files that define your workflows. For example, create a file named `ci-cd.yml`.

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v2

    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'

    - name: Install Dependencies
      run: npm install

    - name: Run Tests
      run: npm test
```

In this example, the workflow is triggered on each push to the `main` branch. It checks out the repository, sets up Node.js, installs dependencies, and runs tests.

### 2. Commit and Push

Commit your workflow file and push it to your repository.

```bash
git add .github/workflows/ci-cd.yml
git commit -m "Add CI/CD workflow"
git push origin main
```

### 3. Check Workflow Status

Visit the "Actions" tab on your GitHub repository to see the status of your workflow. GitHub Actions will automatically run the defined workflow whenever a push event occurs on the specified branch.

## Conclusion

GitHub Actions simplifies the automation of your software development workflows. By defining workflows in your repository, you can automate tasks and streamline your development process. Explore the [GitHub Actions Marketplace](https://github.com/marketplace?type=actions) to discover and use pre-built actions to enhance your workflows.

Start using GitHub Actions today to save time and ensure the reliability of your codebase!


# Automating Weather Updates with GitHub Actions

GitHub Actions provides a powerful way to automate various tasks, and in this tutorial, we'll walk through setting up a GitHub Action to run a Python script (`meteo.py`) that fetches weather information and notifies you via Telegram. This workflow will run on a schedule.

## Scheduling the Workflow

First, let's set up the schedule for our workflow. We want it to run every six hours. Add the following YAML configuration to your `.github/workflows/run-meteo.yml` file:

```yaml
name: Run meteo.py

on:
  schedule:
    - cron: '0 */6 * * *' # At 00:00 on Monday

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # ... rest of the steps ...
```

This configuration uses a cron expression to trigger the workflow every six hours.

## Workflow Steps

Now, let's break down the steps in our workflow:

1. **Checkout Repository:**
   ```yaml
   - name: Checkout repo content
     uses: actions/checkout@v2
   ```
   This step checks out the repository content to the GitHub runner.

2. **Setup Python:**
   ```yaml
   - name: Setup Python
     uses: actions/setup-python@v4
     with:
       python-version: '3.9'
   ```
   Sets up the required Python version for our script.

3. **Install Python Packages:**
   ```yaml
   - name: Install Python packages
     run: |
       python -m pip install --upgrade pip
       pip install -r requirements.txt
   ```
   Installs necessary Python packages specified in `requirements.txt`.

4. **Execute Python Script:**
   ```yaml
   - name: Execute py script
     run: |
       python meteo.py
       echo "TEMPERATURE=$(cat meteo.txt | grep TEMPERATURE | cut -d= -f2)" >> $GITHUB_ENV
       echo "HUMIDITY=$(cat meteo.txt | grep HUMIDITY | cut -d= -f2)" >> $GITHUB_ENV
       echo "FEELS_LIKE=$(cat meteo.txt | grep FEELS_LIKE | cut -d= -f2)" >> $GITHUB_ENV
       echo "COMMENT=$(grep -oP \"(?<=COMMENT=).*\" meteo.txt)" >> $GITHUB_ENV
   ```
   Executes the Python script (`meteo.py`) and extracts relevant information to environment variables.

5. **Commit Changes:**
   ```yaml
   - name: Commit files
     run: |
       git config --local user.email "action@github.com"
       git config --local user.name "GitHub Action"
       git add -A
       git diff-index --quiet HEAD || (git commit -a -m "updated logs" --allow-empty)
   ```
   Commits any changes made during the workflow run.

6. **Send Telegram Message:**
   ```yaml
   - name: Send Telegram message to notify
     uses: appleboy/telegram-action@master
     with:
       to: ${{ secrets.TELEGRAM_TO }}
       token: ${{ secrets.TELEGRAM_TOKEN }}
       message: |
         La temperature est de ${{ env.TEMPERATURE }}
         L'humidite est de ${{ env.HUMIDITY }}
         Le ressenti est donc de ${{ env.FEELS_LIKE }}
         ${{ env.COMMENT }}
   ```
   Sends a Telegram message with the weather information.

Ensure you have the necessary secrets (`TELEGRAM_TO` and `TELEGRAM_TOKEN`) set up in your repository.

Now, each time the scheduled event occurs, your Python script will run, and you'll receive weather updates via Telegram. Happy automating!
