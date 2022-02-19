from distutils.command.config import config
from flask import Flask, render_template
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from resources.user import User
from config.config import Config

app = Flask(__name__)
api = Api(app)
app.config = Config(app.config).setFromEnv()
cors = CORS(app, resources={r'/*': {'origins': '*'}})

# route docs
app.register_blueprint(get_swaggerui_blueprint(
  '/docs',
  '/static/swagger.json',
  config={ 'app_name': "Api Platzi" }
))

# route home
@app.route("/")
def index():
  return render_template("index.html")

# routers users
api.add_resource(User, '/users', '/users/<string:username>')

# errorhandler
@app.errorhandler(404)
def page_not_found(e):
  return render_template('errors/404.html'), 404

# init app
if __name__ == '__main__':
  app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
