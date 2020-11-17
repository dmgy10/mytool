from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

#
class News(db.Model):
    """ 新闻模型 """
    __table__name = 'news'



