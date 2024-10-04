'''
A file for freezing the application in its current state (so that it can be deployed onto Netlify)
'''

from flask_frozen import Freezer
from app import app

freezer = Freezer(app)
if __name__ == '__main__':
    freezer.freeze()