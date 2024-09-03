from src.main import app

if __name__ == "__main__":
    import uvicorn

    _ = app
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
