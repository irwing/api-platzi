from dotenv import dotenv_values

class Config():

  def __init__(self, config):
    config.update(
      ENV=dotenv_values(".env")['ENVIROMENT'],
      SECRET_KEY=dotenv_values(".env")['SECRET_KEY'],
      DEBUG=dotenv_values(".env")['DEBUG'],
      HOST=dotenv_values(".env")['HOST'],
      PORT=dotenv_values(".env")['PORT']
    )
    self.config = config

  def setFromEnv(self):
    return self.config
