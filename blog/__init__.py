import logging
from logging.handlers import RotatingFileHandler
from redis import StrictRedis
from flask import Flask, render_template, g
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

# from apps.utils.common import user_login_data
from config import config

# 数据库
db = SQLAlchemy()
redis_store = None


def create_app(config_name):
    """通过传入不同的配置名字，初始化其对应配置的应用实例"""

    # 配置项目日志
    setup_log(config_name)

    app = Flask(__name__)

    # 配置
    app.config.from_object(config[config_name])
    # 配置数据库
    db.init_app(app)
    # 配置redis
    global redis_store
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    # 开启csrf保护
    CSRFProtect(app)
    # 设置session保存位置
    Session(app)

    # from apps.utils.common import do_index_class
    # 添加自定义过滤器
    # app.add_template_filter(do_index_class, "indexClass")

    # @user_login_data

    # @app.errorhandler(404)
    # def page_not_found(_):
    # user = g.user
    # data = {"user_info": user.to_dict() if user else None}
    # return render_template('news/404.html', data=data)
    # return app

    @app.after_request
    def after_request(response):
        # 生成随机的csrf_token的值
        csrf_token = generate_csrf()
        # 设置一个cookie
        response.set_cookie("csrf_token", csrf_token)
        return response

    # 注册蓝图
    # 首页
    from blog.modules.index import index_bp
    app.register_blueprint(index_bp)

    # 博客页
    from blog.modules.article import article_bp
    app.register_blueprint(article_bp)

    return app


def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
