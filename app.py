
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from App.app_init_ import app

if __name__ == '__main__':
  app.run(debug=True)

