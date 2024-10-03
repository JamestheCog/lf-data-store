'''
Contains several routes for interacting with a database
'''
from flask import Blueprint, render_template
from utils import db
import os

dashboard = Blueprint('dashboard', __name__, template_folder = 'templates')

@dashboard.route('/dashboard', methods = ['GET'])
def get_dashboard():
    submissions, _ = db.fetch_data(os.getenv('ACCESS_KEY'), os.getenv('FERNET_KEY'))
    return(render_template('dashboard/index.html', num_responses = len(submissions)), 200)