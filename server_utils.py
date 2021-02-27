import base64, json, jwt

### ERRORS
class InvalidJWT(Exception):
  def __init__(self, token):
    self.token = token

class ExpiredJWT(Exception):
  def __init__(self, token):
    _, payload, _ = token.split(".")
    payload = json.loads(base64.b64decode(payload + "==").decode("utf-8"))
    self.expiry = payload["exp"]

def load_file(filename):
  with open(filename, "r") as f:
    return f.read()
  
def _verify_jwt(token, key):
  try:
    return jwt.decode(token, key, algorithms = ["HS256"])
  except jwt.exceptions.ExpiredSignatureError:
    raise ExpiredJWT(token)
  except:
    raise InvalidJWT(token)

def _make_jwt(payload, key):
  return jwt.encode(payload, key, algorithm = "HS256").decode("utf-8")