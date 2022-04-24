from flask import Blueprint

main = Blueprint("main", __name__)

from liveexpress.main import routes
