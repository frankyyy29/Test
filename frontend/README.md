# Intersys I3 Payroll - React Frontend

A modern React dashboard for the Intersys payroll application.

## Features

- **Employee Management** — Create and list employees
- **Attendance Tracking** — Log and view attendance records
- **Payroll Processing** — Run payroll and manage payslips
- **PDF Downloads** — Download individual payslips as PDF
- **Excel Export** — Download payroll summary as Excel

## Local Development

### Prerequisites

- Node.js 16+ and npm

### Setup

```bash
cd frontend
npm install
```

### Configure API Endpoint

Create a `.env` file (or copy `.env.example`):

```bash
cp .env.example .env
```

Update `REACT_APP_API_URL` if needed (default: `https://intersys-payroll.onrender.com`).

### Run Locally

```bash
npm start
```

The app will open at `http://localhost:3000`.

### Build for Production

```bash
npm run build
```

Creates an optimized production build in the `build/` directory.

## Deployment

### Option 1: Deploy to Vercel (Recommended)

1. Push the repo to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project" and select your GitHub repo
4. Set:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. Add Environment Variable:
   - `REACT_APP_API_URL`: `https://intersys-payroll.onrender.com` (or your API URL)
6. Click "Deploy"

### Option 2: Deploy to Netlify

1. Push the repo to GitHub
2. Go to [netlify.com](https://netlify.com) and connect your GitHub repo
3. Set:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `build`
4. Add Environment Variable:
   - `REACT_APP_API_URL`: `https://intersys-payroll.onrender.com`
5. Click "Deploy"

### Option 3: Deploy to Render (Static Site)

1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Create a new Static Site on Render
3. Set:
   - **Public directory**: `build`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: (leave blank for static sites)
4. Add Environment Variable:
   - `REACT_APP_API_URL`: `https://intersys-payroll.onrender.com`
5. Deploy

## Testing

```bash
npm test
```

Runs the test suite in interactive watch mode.

## Notes

- The frontend communicates with the backend API at `https://intersys-payroll.onrender.com`
- API URL can be configured via the `REACT_APP_API_URL` environment variable
- CORS must be enabled on the backend (or use a proxy)

## Support

For issues with the API, refer to the main [README.md](../README.md).
