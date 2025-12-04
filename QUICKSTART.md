# Semantic Alchemy - Web App Quickstart

This guide will help you run the web-based version of Semantic Alchemy with **hot reloading** enabled.

## Prerequisites

- Python 3.8+ installed
- Node.js 18+ installed
- Git initialized (done!)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (backend framework)
- Uvicorn (ASGI server with hot reload)
- Other required packages

### 2. Frontend Dependencies Already Installed

The React + Vite frontend has already been set up and dependencies installed!

## Running the Application

You need to run **two servers** simultaneously for full hot-reload functionality:

### Terminal 1: Backend Server (FastAPI)

```bash
python api.py
```

This will start the FastAPI backend on **http://localhost:8000** with hot-reload enabled.

**Backend Hot Reload**: Any changes you make to Python files (`.py`) will automatically restart the server!

### Terminal 2: Frontend Server (Vite)

```bash
cd frontend
npm run dev
```

This will start the Vite dev server on **http://localhost:5173**

**Frontend Hot Reload (HMR)**: Any changes you make to React files will instantly update in the browser without refresh! Component state is preserved during updates.

## Accessing the Application

1. Open your browser to: **http://localhost:5173**
2. The frontend will communicate with the backend on port 8000
3. You should see your Semantic Alchemy game!

## Testing Hot Reload

### Backend Changes:
1. Open `api.py`
2. Change something (like the welcome message in the root endpoint)
3. Save the file
4. Watch the terminal - you'll see the server restart
5. Refresh your browser to see changes

### Frontend Changes:
1. Open `frontend/src/App.jsx` or `frontend/src/App.css`
2. Change colors, text, layout, etc.
3. Save the file
4. **Instantly see changes in browser** - no refresh needed!

## API Documentation

With the backend running, visit:
- **http://localhost:8000/docs** - Interactive API documentation (Swagger UI)
- **http://localhost:8000/redoc** - Alternative API documentation

## Project Structure

```
.
├── api.py                    # FastAPI backend (hot-reload enabled)
├── alchemy_engine/           # Game logic & database
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styles
│   │   └── api.js           # API service layer
│   └── package.json
├── requirements.txt          # Python dependencies
└── QUICKSTART.md            # This file!
```

## Troubleshooting

### Backend won't start
- Make sure you installed Python dependencies: `pip install -r requirements.txt`
- Check if port 8000 is already in use

### Frontend shows connection error
- Make sure the backend is running on port 8000
- Check browser console for CORS errors

### Hot reload not working
- **Backend**: Make sure you're running with `python api.py` (not `uvicorn api:app` without reload flag)
- **Frontend**: Make sure you're using `npm run dev` (not `npm run build`)

## Development Workflow

1. Start both servers (backend + frontend)
2. Make changes to your code
3. Changes appear automatically:
   - **Frontend**: Instant (HMR)
   - **Backend**: ~1-2 seconds (server restart)
4. Use git to track your changes:
   ```bash
   git add .
   git commit -m "Your message"
   ```

## What's Next?

- The pygame GUI is still available in `gui_main.py` if you want to compare
- All game logic is in `alchemy_engine/` and works with both interfaces
- Customize the UI in `frontend/src/App.jsx` and `frontend/src/App.css`
- Add new API endpoints in `api.py`
- Changes to the alchemy engine will be reflected in both GUIs

Enjoy building with instant feedback!
