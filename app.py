from liveexpress import create_app, db
from liveexpress.config import Config
from liveexpress.models import User, Post
from flask_migrate import Migrate
app = create_app(Config)

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, user=User, post=Post)
if __name__ == "__main__":
    app.run(debug=True)