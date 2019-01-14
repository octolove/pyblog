from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
app.config.from_object('config')

engine = create_engine("mysql+pymysql://root:root123@127.0.0.1:3306/blogdb?charset=utf8",encoding='utf-8',echo=True)
Base=declarative_base()

from blog import views