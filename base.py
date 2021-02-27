from flask import Flask, flash, json, make_response, redirect, render_template, request
from flask_cors import CORS

from server_utils import _verify_jwt, _make_jwt, load_file, InvalidJWT, ExpiredJWT

import argon2, random

### FOLDER PATHS
KEYS_FOLDER_PATH = "/home/hyper-neutrino/workspace/system/keys/"

### PATHS
SECRET_KEY_PATH = KEYS_FOLDER_PATH + "secret-key.pem"

app = Flask(__name__)
CORS(app)

app.secret_key = SECRET_KEY = load_file(SECRET_KEY_PATH)

def verify_jwt(token):
  return _verify_jwt(token, SECRET_KEY)

def make_jwt(payload):
  return _make_jwt(payload, SECRET_KEY)

def random_salt(length = 16):
  salt = bytes()
  for _ in range(length):
    salt += bytes([random.randint(0, 255)])
  return salt

def passhash(string, salt):
  return argon2.argon2_hash(string, salt)