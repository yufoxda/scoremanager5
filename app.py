import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'App'))



from App.app_init_ import app

if __name__ == '__main__':
  app.run(debug=True)

