from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
import database
import router2
import schemas
from fastapi_mcp import FastApiMCP
import uvicorn

# Create all database tables on startup
# create_db_and_tables()

app = FastAPI(title="Smart Doctor Assistant")

# --- CORS Middleware ---
# This allows the React frontend (running on a different port) to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # The origin of your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include API Routers ---
# This makes the endpoints in routers.py available in our app
app.include_router(router2.router, prefix="/api", tags=["tools"])

# --- Session Management for Conversation History ---
# A simple in-memory dictionary to store conversation history per session
session_store = {}


# --- MCP Server Setup ---
# This is the magic that exposes our API endpoints as MCP tools
mcp = FastApiMCP(
    app,
    name="DoctorAppointmentTools",
    description="A set of tools for managing doctor appointments, checking schedules, and generating reports.",
)
mcp.mount_http() # This creates the /mcp endpoint

# --- Run the application ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)