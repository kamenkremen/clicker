from flask import Flask

from website import create_app, create_session


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)