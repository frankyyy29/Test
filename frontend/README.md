# Intersys I3 Payroll - React Frontend

A modern React dashboard for the Intersys payroll application, built with Vite for fast builds and optimal compatibility.

## Features

- **Employee Management** — Create and list employees
- **Attendance Tracking** — Log and view attendance records
- **Payroll Processing** — Run payroll and manage payslips
- **PDF Downloads** — Download individual payslips as PDF
- **Excel Export** — Download payroll summary as Excel

## Local Development

### Prerequisites

- Node.js 18+ and npm

### Setup

```bash
cd frontend
npm install
```

### Configure API Endpoint

The frontend connects to the backend API at `https://intersys-payroll.onrender.com` by default.
To configure locally, update `src/api.js` and change the `API_URL` constant if needed.

### Run Locally

```bash
npm run dev
```

The app will open at `http://localhost:3000`.

### Build for Production

```bash
npm run build
```

Creates an optimized production build in the `dist/` directory.

## Deployment

### Option 1: Deploy to Render (Docker - Recommended)

The frontend includes a `Dockerfile` for containerized deployment:

1. Push the repo to GitHub
2. Go to [dashboard.render.com](https://dashboard.render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Set:
   - **Root Directory**: `frontend` (optional)
   - **Environment**: `Docker`
   - **Dockerfile Path**: `frontend/Dockerfile` or `./Dockerfile` (depending on repo structure)
   - **Start Command**: Leave empty (Dockerfile specifies it)
6. Click "Create Web Service"

The service will build and deploy automatically. It will be available at the Render-provided URL.

### Option 2: Deploy to Vercel

1. Push the repo to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project" and select your GitHub repo
4. Set:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Click "Deploy"

### Option 3: Deploy to Netlify

1. Push the repo to GitHub
2. Go to [netlify.com](https://netlify.com) and connect your GitHub repo
3. Set:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
4. Click "Deploy"

### Option 4: Deploy to Render (Static Site - Legacy)

1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Create a new Static Site on Render
3. Set:
   - **Public directory**: `dist`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: (leave blank for static sites)
4. Deploy

## Tech Stack

- **Framework**: React 18.2.0 with React Router 6.10.0
- **Build Tool**: Vite 5.0.0 (fast, no Node.js version conflicts)
- **HTTP Client**: Axios
- **Styling**: CSS3 (plain CSS, no additional framework)

The migration from react-scripts to Vite eliminates Node.js version compatibility issues and provides significantly faster builds.

## Environment Variables

No environment variables are required. The frontend auto-detects the API URL:
- **Local**: Connects to `http://localhost:10000` when running with `npm run dev`
- **Production**: Connects to the backend URL as deployed (Render, etc.)

Update `src/api.js` if you need to override the API base URL.
## Notes

- The frontend communicates with the backend API at `https://intersys-payroll.onrender.com`
- API URL can be configured via the `REACT_APP_API_URL` environment variable
- CORS must be enabled on the backend (or use a proxy)

## Support

For issues with the API, refer to the main [README.md](../README.md).
