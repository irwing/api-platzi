from flask import Flask, render_template, request
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from dotenv import dotenv_values

# include ScrapingPlatzi
from libs import scraping

# get environment variables
config = dotenv_values(".env")

print(config["PORT"])

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config={
    'app_name': "My Rest App"
  }
)

# route docs
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# router /
@app.route("/")
def index():
  return render_template("404.html")

# routers users
@app.route('/users/<username>')
def users(username):

  # validate if header api-key not exists or if diferent to config["API_KEY"]
  if (request.headers.get("api-key") != config["APIKEY"]):
    return render_template("401.html"), 401

  try:
    Scraping = scraping.ScrapingPlatzi(username)
    data = Scraping.scraping()
  except Exception as e:
    print(e)
    return render_template("500.html"), 500

  if(data == 404):
    return render_template("404.html"), 404

  return data

# error 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
  app.run(debug=config['DEBUG'], host=config['HOST'], port=config['PORT'])
