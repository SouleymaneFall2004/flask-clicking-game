import os

from route import *

if __name__ == '__main__':
    if not os.path.exists('clicker.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
