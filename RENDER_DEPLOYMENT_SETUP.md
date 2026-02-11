# Automated Render Deployment Setup

This guide sets up automatic deployments to Render whenever you push to GitHub.

## Prerequisites

- deployed both services to Render (backend and frontend)
- Render account with access to both services

## Step 1: Get Your Render API Key

1. **Visit** https://dashboard.render.com/account/api-keys
2. **Click "Create API Key"**
3. **Name it** (e.g., "GitHub Actions")
4. **Copy the key** (save it - you won't see it again!)

## Step 2: Get Service IDs

For each service (backend & frontend):

1. **Visit** https://dashboard.render.com
2. **Click the service** (e.g., "intersys-payroll-backend")
3. **Copy the Service ID** from the URL bar:
   - URL format: `https://dashboard.render.com/services/srv-xxxxxxxxxxxxx`
   - Copy: `srv-xxxxxxxxxxxxx`
4. **Repeat for frontend service**

## Step 3: Add GitHub Secrets

1. **Visit** https://github.com/frankyyy29/Test/settings/secrets/actions
2. **Click "New repository secret"** for each:

   ```
   Name: RENDER_API_KEY
   Value: (your API key from Step 1)
   ```

   ```
   Name: RENDER_BACKEND_SERVICE_ID
   Value: srv-xxxxxxxxxxxxx (backend service ID)
   ```

   ```
   Name: RENDER_FRONTEND_SERVICE_ID
   Value: srv-xxxxxxxxxxxxx (frontend service ID)
   ```

3. **Click "Add secret"** for each

## Step 4: Test the Deployment

1. **Make any change** to your repo (e.g., update README)
2. **Commit and push** to `main`:
   ```bash
   git add .
   git commit -m "test: trigger deployment"
   git push origin main
   ```

3. **Check GitHub Actions**:
   - Go to https://github.com/frankyyy29/Test/actions
   - Watch the "Deploy to Render" workflow run
   - Both backend and frontend should deploy automatically

4. **Verify on Render**:
   - https://dashboard.render.com
   - Check both services for deployment status
   - Both should show "Active" after a few minutes

## Troubleshooting

### Deployment doesn't trigger
- Verify all 3 secrets are set correctly
- Check spelling: `RENDER_API_KEY`, `RENDER_BACKEND_SERVICE_ID`, `RENDER_FRONTEND_SERVICE_ID`
- Service IDs must start with `srv-`

### Deployment fails with "Unauthorized"
- API key may have expired
- Generate a new key and update the `RENDER_API_KEY` secret

### Service doesn't update
- Check Render dashboard for deployment logs
- Verify Docker builds complete successfully
- Check that `render.yaml` or Dockerfile are correct

## How It Works

When you push to `main`:

1. GitHub Actions workflow triggers
2. Calls Render API to deploy backend service
3. Calls Render API to deploy frontend service
4. Both services rebuild and redeploy from your latest code
5. Takes ~2-5 minutes total

## Manual Deploy (No Automation)

Without secrets configured, just:

1. Commit and push to GitHub
2. Visit https://dashboard.render.com
3. Click each service and hit the **"Deploy"** button

---

Once you have the secrets configured, all future pushes to `main` will automatically deploy both services! 🚀
