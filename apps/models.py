from werkzeug.security import generate_password_hash, check_password_hash

from . import db, constants
from datetime import datetime


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class Category(db.Model):
    """分类"""
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64))  # 分类名
    post_list = db.relationship('Post', backref='category', lazy='dynamic')

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "name": self.name
        }
        return resp_dict


class Tag(db.Model):
    """标签"""
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)  # 标签编号
    name = db.Column(db.String(64))  # 标签名
    post_list = db.relationship('Post', backref='category', lazy='dynamic')

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "name": self.name
        }
        return resp_dict


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)  # 是否是管理员
    post_list = db.relationship(
        'Post', backref='User', lazy='lazy'
    )

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
            "post_count": self.post_list.count()
        }
        return resp_dict

    def to_admin_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "register": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return resp_dict


class Comment(BaseModel, db.Model):
    """评论"""
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 用户id
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)  # 新闻id
    body = db.Column(db.Text, nullable=False)  # 评论内容
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))  # 父评论id
    parent = db.relationship("Comment", remote_side=[id])  # 自关联
    like_count = db.Column(db.Integer, default=0)  # 点赞条数

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "parent": self.parent.to_dict() if self.parent else None,
            "user": User.query.get(self.user_id).to_dict(),
            "news_id": self.news_id,
            "like_count": self.like_count
        }
        return resp_dict


class CommentLike(BaseModel, db.Model):
    """评论点赞"""
    __tablename__ = "comment_like"
    comment_id = db.Column("comment_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True)  # 评论编号
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)  # 用户编号


class Post(BaseModel, db.Model):
    """文章"""
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)  # 文章编号
    title = db.Column(db.String(128), nullable=False)  # 文章标题
    index_image_url = db.Column(db.String(256))  # 新闻列表图片路径
    body = db.Column(db.Text, nullable=False)  # 内容
    views = db.Column(db.BigInteger, nullable=False)  # 阅读量
    excerpt = db.Column(db.String(256), nullable=True)  # 文章摘要
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 分类
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 标签
    author = db.Column(db.Integer, db.ForeignKey('user.id'))  # 作者
    comments = db.relationship("Comment", lazy="dynamic")  # 当前新闻的所有评论

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "body": self.body,
            "comments_count": self.comments.count(),
            "views": self.views,
            "category": self.category.to_dict(),
            "index_image_url": self.index_image_url,
            "author": self.user.to_dict() if self.user else None
        }
        return resp_dict
