from flask import Flask

app = Flask(__name__)

from routes import square
from routes import lazy_developer
from routes import ctf
from routes import greedy
from routes import maze
from routes import pie_chart

