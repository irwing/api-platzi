from flask import request, make_response, render_template
from flask_restful import Resource

from libs import authentication, scraping

class User(Resource):

  def __init__(self):
    auth = authentication.Auth(request)
    self.validate_key_secret = auth.validationApiKey()

  def get(self, username):
    try:
      if(self.validate_key_secret == False):
        return make_response(
          render_template('errors/401.html'),
          401, {'Content-Type': 'text/html'}
        )
    
      Scraping = scraping.ScrapingPlatzi(username)
      return Scraping.scraping()
    except Exception as e:
      return make_response(
        render_template('errors/500.html'),
        500, {'Content-Type': 'text/html'}
      )
