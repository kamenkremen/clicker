from flask import Flask
from flask_ngrok import run_with_ngrok
from website import create_app, create_session


app = create_app()
run_with_ngrok(app)

if __name__ == '__main__':
    app.run()