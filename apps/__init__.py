import logging
from logging.handlers import RotatingFileHandler

from flask_session import Session
from redis import StrictRedis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_wtf import CSRFProtect

# from flask_wtf.csrf import generate_csrf
# 初始化SQLAlchemy对象
db = SQLAlchemy()
# 设置默认redis对象
redis_store = None


def create_app(config_name):
    """
    根据传入的配置名字初始化对应配置的应用实例
    :param config_name: 配置名
    :return: app: 对应配置的应用实例
    """
    # 配置日志
    setup_log(config_name)
    # 初始化Flask实例
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

    # 注册蓝图
    # 主页
    from apps.modules.index import index_bp
    app.register_blueprint(index_bp)
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
