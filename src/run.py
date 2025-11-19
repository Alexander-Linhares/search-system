import sys
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(base_dir, 'src'))

from app import app


if __name__ == "__main__":
    app.run(debug=True)