import uvicorn
import os

if __name__ == "__main__":
    print("Starting Legal Triage OpenEnv Local Server...")
    print("Open http://127.0.0.1:8000 in your browser to see the frontend.")
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
