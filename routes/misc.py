'''
A file to contain miscellaneous routes for other parts of the application.
'''

from flask import Blueprint

misc = Blueprint('misc', __name__)

@misc.route('/ping', methods = ['GET'])
def ping():
    '''
    For a chron job to use; returns the string 'pong' and an "ok" status code.
    '''
    return('pong', 200)