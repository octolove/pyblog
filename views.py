#!/--*--coding:utf-8--*--
import time,json,re,uuid,os
from blog import app
from flask import request
from flask import render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from blog.models import Article, Customer, Comment,UserInfo
from blog import config
from blog.util import DbUtil

@app.before_request
def accessFilter():
    #处理
    publicUrl = ['article']
    if not session or not session['username']:
        if request.url.split('/')[3] in publicUrl:
            return render_template('login.html', title='登录', message='请您先登录')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    session=DbUtil().getSession()
    userlist=session.query(UserInfo).all()
    articlelist=session.query(Article).all()

    #分页

    return render_template('index.html', name='cxd', title='穷开心', articlelist=articlelist, userlist=userlist)


@app.route('/login', methods=['POST', 'GET'])
def login():
    dbsession=DbUtil().getSession()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        u=dbsession.query(UserInfo).filter_by(username=username, passwd=password).first()
        if u:
            ##登陆成功加入session
            session['username'] = username
            return redirect('/index')

    #abort(404)
    return render_template('login.html', title='登录', message='欢迎加入我们')


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    session=DbUtil().getSession()
    if request.method == 'POST':
        #保存图片
        f = request.files['image']
        fname = secure_filename(f.filename)
        f.save(os.path.join(config.image_url, fname))

        u = Customer()
        u.username = request.form.get('username')
        u.password = request.form.get('password')
        u.birthday = request.form.get('birthday')
        u.image = fname
        u.description = request.form.get('description')
        u.sexs = request.form.get('sexs')

        session.add(u)
        session.commit()

        return redirect(url_for('userlist'))

    return render_template('reg.html', title='reg form')


@app.route('/userlist')
def userlist():
    session=DbUtil().getSession()
    userlist = session.query(Customer).all()
    return render_template('userlist.html', title='user list data', userlist=userlist)


@app.route('/article', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
        db=DbUtil().getSession()
        arti = Article()
        arti.title = request.form.get('title')
        arti.article = request.form.get('content')
        arti.author = session['username']
        arti.creatime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        arti.goods = 0
        arti.bads = 0
        db.add(arti)
        db.commit()

        return redirect('/index')

    return render_template('articleEdit.html', title='user list data')


@app.route('/view/<int:id>', methods=['POST', 'GET'])
def viewArticle(id):
    if id:
        session=DbUtil().getSession()
        article = session.query(Article).filter(Article.id==id).first()

        #获取评论
        comments = session.query(Comment).filter(Comment.articleid==id).all()

        return render_template('viewArticle.html', title='user list data', article=article, comments=comments)


#初始化uedit参数
@app.route('/upload', methods=['POST', 'GET'])
def editArticle():
    result = None
    action = request.args.get('action')
    with open(os.path.join(app.static_folder, 'ueditor', 'php', 'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}

    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    if action in ('uploadimage', 'uploadvideo', 'uploadfile'):
        upfile = request.files['upfile']
        fname = secure_filename(upfile.filename)
        #图片后缀
        prefix = fname.split(".")[-1]
        newFileName = re.sub('-', '', str(uuid.uuid1())) + "." + prefix
        upfile.save(os.path.join(config.image_url, newFileName))

        result = {
            "state": "SUCCESS",
            "url": "/static/upload_image/" + newFileName,
            "title": newFileName,
            "original": newFileName
        }
        return json.dumps(result)

    return json.dumps(result)


@app.route('/ueditor', methods=['POST', 'GET'])
def ueditor():
    return render_template('articleEdit.html', title='editArticle')


@app.route('/comment', methods=['POST', 'GET'])
def comment():
    session=DbUtil().getSession()
    username = request.form.get('username')
    content = request.form.get('content')
    artid = request.form.get('artid')

    comm = Comment()
    comm.articleid = artid
    comm.commentdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    comm.content = content
    comm.username = username

    session.add(comm)
    session.commit()

    return redirect('/view/%s' % artid)


@app.errorhandler(404)
def page_not_fond(error):
    return render_template('page_not_found.html'), 404


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))