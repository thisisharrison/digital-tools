from app.main import app
import os

if __name__ == "__main__":
    app.run()
    socketio.run(app, port=int(os.environ.get('PORT', '5000')))