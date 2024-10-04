from flask import Flask

# Import the routes here:
from routes.db import db
from routes.misc import misc

## Application start and route registration:
app = Flask(__name__)
app.register_blueprint(db)
app.register_blueprint(misc)

if __name__ == '__main__':
    app.run()