from flask import Flask, g
from routes.user import user_bp
from routes.boards import boards_bp
from routes.uploads import uploads_bp

app = Flask(__name__)

# Закриття підключення після завершення запиту
@app.teardown_request
def teardown_request(exception):
    db = g.pop('db', None)
    if db is not None:
        db.client.close()

# Реєстрація Blueprint'ів
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(boards_bp, url_prefix='/api/boards')
app.register_blueprint(uploads_bp, url_prefix='/api/upload')

if __name__ == '__main__':
    app.run(debug=True)