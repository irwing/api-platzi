from flask import current_app as app

class Auth():

  def __init__(self, request):
    self.request = request
    self.secret_key = request.headers.get("secret_key")

  def validationApiKey(self):
    return (self.secret_key == app.config["SECRET_KEY"])
