from src.api.main import app

# This is the entry point for Hugging Face Spaces
# Hugging Face will look for a variable called "app" in this file

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)