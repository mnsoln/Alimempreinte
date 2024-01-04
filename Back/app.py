from flask import Flask
# from Alimempreinte_server import app
from server_app import app

if __name__ == '__main__':
    app.run(debug=True)