from hello import app
from flask import current_app


a = app.url_map
print(a)