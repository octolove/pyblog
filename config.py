#!/--*--coding:utf-8--*--
CSRF_ENABLED = True
SECRET_KEY = 'test'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]



#图片存放路径
image_url = 'E:/pyWorker/flaskApp/app/static/upload_image'

#图片显示路径
image_path = '/static/upload_image/'

