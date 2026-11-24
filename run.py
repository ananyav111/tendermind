import uvicorn
import os
import sys

# Ensure repository root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Starting TenderMind Agentic AI & MCP Platform")
    print("   Open Dashboard at: http://localhost:8000")
    print("   API Documentation: http://localhost:8000/docs")
    print("=" * 70)
    uvicorn.run("tendermind.api.app:app", host="127.0.0.1", port=8000, reload=True)
