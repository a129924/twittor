from twittor import create_app
from twittor.models import User, Tweet

app = create_app()

if __name__ == '__main__':
    app.run(debug = True)