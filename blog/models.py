from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from blog import constants
from . import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    qq_number = db.Column(db.String(11), unique=True, nullable=False)  # qq号
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)  # 是否是管理员
    post_list = db.relationship('Post', backref='user', lazy='dynamic')  # 当前用户所发布的文章

    @property
    def password(self):
        raise AttributeError("当前属性不可读")

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "avatar_url": constants.QINIU_DOMIN_PREFIX + self.avatar_url if self.avatar_url else "",
            "qq_number": self.qq_number,
        }
        return resp_dict

    def to_admin_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "mobile": self.mobile,
            "register": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return resp_dict


class Post(BaseModel, db.Model):
    """博文"""
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)  # 博文编号
    source = db.Column(db.String(64), nullable=False)  # 新闻来源
    title = db.Column(db.String(256), nullable=False)  # 博文标题
    digest = db.Column(db.String(512), nullable=False)  # 博文摘要
    content = db.Column(db.Text, nullable=False)  # 博文内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    index_image_url = db.Column(db.String(256))  # 博文列表图片路径
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))  # 分类id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 当前博文的作者id
    status = db.Column(db.Integer, default=0)  # 当前博文状态 如果为0代表可对外展示，1代表隐藏
    comments = db.relationship("Comment", lazy="dynamic")  # 当前博文的所有评论

    def to_review_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
        }
        return resp_dict

    def to_basic_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "index_image_url": self.index_image_url,
            "clicks": self.clicks,
            "comments": self.comments.count()
        }
        return resp_dict

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "comments_count": self.comments.count(),
            "clicks": self.clicks,
            "category": self.category.to_dict(),
            "index_image_url": self.index_image_url,
            "author": self.user.to_dict() if self.user else None
        }
        return resp_dict


class Comment(BaseModel, db.Model):
    """评论"""
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 用户id
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)  # 博文id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))  # 父评论id
    parent = db.relationship("Comment", remote_side=[id])  # 自关联

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "parent": self.parent.to_dict() if self.parent else None,
            "user": User.query.get(self.user_id).to_dict(),
            "post_id": self.post_id,
        }
        return resp_dict


class Category(BaseModel, db.Model):
    """博文分类"""
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    post_list = db.relationship('Post', backref='category', lazy='dynamic')

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "name": self.name
        }
        return resp_dict


class Top(BaseModel, db.Model):
    """置顶博文"""
    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)  # 博文id

    def to_dict(self):
        resp_dict = {
            'post': Post.query.get(self.post_id).to_review_dict(),
        }
        return resp_dict
