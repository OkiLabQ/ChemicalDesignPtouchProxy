from dotenv import load_dotenv
from app.index import app

if __name__ == "__main__":
    load_dotenv(override=True)
    app.run(host="localhost", port=8080)