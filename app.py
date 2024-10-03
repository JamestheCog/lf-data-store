from flask import Flask, render_template

# Import the routes here:
from routes.db import db
from routes.dashboard import dashboard

## Application start and route registration:
app = Flask(__name__)
app.register_blueprint(db)
app.register_blueprint(dashboard)

## Error handling in the application (meant for when somebody accesses the application):
@app.errorhandler(403)
def forbidden_access(e):
    return(render_template('./errors/page-403.html', e = e), 403)

@app.errorhandler(404)
def page_not_found(e):
    return(render_template('./errors/page-404.html', e = e), 404)

@app.errorhandler(500)
def internal_server_error(e):
    return(render_template('./errors/page-500.html', e = e), 500)