from distutils.log import debug
from config import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)