import uvicorn
from fastapi.staticfiles import StaticFiles
from api.index import app

# Mount the current directory at the root to serve index.html
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    print("Starting local server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
