
from sqlalchemy.orm import sessionmaker
from blog import app,engine
import os,time,datetime



class DbUtil:
    def __init__(self):
        Session_class = sessionmaker(bind=engine)
        self.session = Session_class()

    def getSession(self):
        return self.session

def getRandom():
    t = time.time()
    return lambda:int(round(t * 1000))
