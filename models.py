#-*- coding=utf-8 -*-

from blog import engine,Base
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey,SmallInteger,CHAR
from sqlalchemy.orm import relationship


class UserInfo(Base):
    __tablename__ = 'userinfo'
    __table_args__ = {"useexisting": True}

    id = Column(Integer(),primary_key=True)
    username = Column(String(32))
    passwd = Column(String(32))
    address = Column(String(32))
    phone=Column(String(32))

    def __repr__(self):
        return '<username %s>' % self.username

class Article(Base):
    __tablename__ = 'article'
    __table_args__ = {"useexisting": True}

    id =Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    article = Column(Text(), nullable=False)
    author = Column(String(20), nullable=False)
    creatime = Column(DateTime())
    goods = Column(SmallInteger)
    bads = Column(SmallInteger)
    comments= relationship("Comment", backref="Article")

    def __repr__(self):
        return '%s-%s-%s' % (self.id,self.title,self.article)


class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = {"useexisting": True}

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password =Column(String(20))
    birthday = Column(DateTime())
    image = Column(String(100))
    description = Column(Text())
    sexs = Column(CHAR(1))

    def __repr__(self):
        return '<Customer %r>' % self.username


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = {"useexisting": True}

    id =Column(Integer, primary_key=True)
    username=Column(String(20))
    content=Column(Text())
    commentdate = Column(DateTime())
    articleid = Column(Integer,ForeignKey('article.id'))


if __name__ == '__main__':
    #创建数据库
    Base.metadata.create_all(engine)
