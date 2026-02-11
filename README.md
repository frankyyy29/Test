# Intersys I3 Payroll (MVP FastAPI scaffold)

This repository contains a minimal FastAPI scaffold for a payroll application (attendance and non-attendance employees).

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

2. Run the app locally:

```bash
uvicorn src.app.main:app --reload
```

Run with Docker:

```bash
docker build -t intersys-payroll:latest .
docker run -p 10000:10000 -e PORT=10000 --name payroll intersys-payroll:latest
# then visit http://localhost:10000/health
```

Deploying on Render using Docker

1. Use the provided `Dockerfile` in the repo root.
2. In Render, create a new Web Service and choose "Docker" as the environment.
3. You can also add the included `render.yaml` manifest to automate service creation via the Render dashboard or the Render CLI.
4. Ensure the `PORT` env var is set (Render will provide it), and optionally set Drive-related env vars if you want uploads.

Alternatively, if you prefer Render to build from source (no Docker), set the service runtime to Python and use the Start Command:

```
gunicorn -k uvicorn.workers.UvicornWorker src.app.main:app -b 0.0.0.0:$PORT
```

Automated Render deployment via GitHub Actions

The repo includes a GitHub Actions workflow (`.github/workflows/render-deploy.yml`) that deploys to Render using the Render CLI whenever you push to `main`.

To enable this:

1. Get your Render API key from https://dashboard.render.com/account/api-keys
2. In your GitHub repo, add these secrets:
   - `RENDER_API_KEY` — your Render API key
   - `RENDER_PROJECT_ID` — (optional) your Render project ID for new service creation
   - `RENDER_SERVICE_ID` — (optional) your Render service ID for updates to existing services
3. The workflow will:
   - Install the Render CLI
   - Create a new service from `render.yaml` (if it doesn't exist), or
   - Deploy to the existing service (if `RENDER_SERVICE_ID` is set)

You can also manually create the service once and then the workflow will keep it updated.

React Frontend Dashboard

A modern React web interface is available in the `frontend/` directory. The dashboard provides:
- Employee management
- Attendance tracking  
- Payroll processing
- Payslip downloads
- Excel export

**Local Development:**

```bash
cd frontend
npm install
npm start
```

The app will open at `http://localhost:3000` and connect to the API at `https://intersys-payroll.onrender.com`.

**Deployment (Docker on Render - Recommended):**

Since the frontend has been migrated to Vite for reliable builds, deployment is now straightforward:

1. **Frontend & Backend together via `render.yaml`**: 
   - Push to GitHub
   - Render automatically detects the manifest and deploys both services
   - Backend runs on port 10000, Frontend on port 3000 (separate services on same project)

2. **Frontend only via Docker**:
   - Create a Web Service in Render
   - Connect your GitHub repo
   - Select "Docker" environment
   - Render will use `frontend/Dockerfile` automatically

3. **Automated via GitHub Actions**:
   - The workflow `.github/workflows/render-deploy.yml` can trigger deployments via Render API
   - Set `RENDER_API_KEY` and `RENDER_SERVICE_ID` secrets in GitHub

**Why Vite instead of react-scripts?**
- react-scripts 5.0.1 has hard dependency conflicts with Node.js 20+ (all modern deployment platforms use Node 20-24)
- Vite is modern, fast, and has zero version conflicts
- Build time: ~2-3 seconds vs 30-60 seconds with react-scripts
- Both are production-ready

**Alternative Deployment Methods (if not using Docker):**

- **Vercel**: Set Root Directory to `frontend`, Build Command to `npm run build`, Output to `dist`
- **Netlify**: Set Base directory to `frontend`, Build command to `npm run build`, Publish to `dist`

See [frontend/README.md](frontend/README.md) for detailed instructions.

**Testing:**

Backend tests:

```bash
pytest -q
```

Frontend tests (if added):

```bash
cd frontend
npm test
```

Data files (SQLite) will be created under `data/payroll.db`. Put that `data/` folder inside a Google Drive-synced directory if you want it backed up.

Google Drive integration (optional)

 - Create a Google Cloud service account with Drive API access and download the JSON key file.
 - Set one of the following environment variables for the app to use the service account:
	 - `GOOGLE_SERVICE_ACCOUNT_FILE` — path to the JSON key file
	 - `GOOGLE_SERVICE_ACCOUNT_JSON` — the JSON content (escaped) as a single env var
 - Optionally set the Drive destination:
	 - `DRIVE_FOLDER_ID` — upload files into this folder id, or
	 - `DRIVE_FOLDER_NAME` — create/find a folder with this name and upload into it
 - Enable uploads by setting `UPLOAD_TO_DRIVE=1` in the environment.

Example (.env):

```
GOOGLE_SERVICE_ACCOUNT_FILE=/secrets/gdrive-sa.json
DRIVE_FOLDER_NAME=IntersysPayrollBackups
UPLOAD_TO_DRIVE=1
```

The exporter will attempt to upload generated payslips and the Excel summary when `UPLOAD_TO_DRIVE` is enabled. Upload failures are logged but won't stop file generation.
