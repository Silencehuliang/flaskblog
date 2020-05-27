from django import db
from flask import request, jsonify, current_app

from blog.models import Post, Comment, User
from blog.modules.comment import comment_bp
from blog.utils.response_code import RET


@comment_bp.route('/comment', methods=["POST"])
def add_post_comment():
    """添加评论"""

    # 获取参数
    data_dict = request.json
    user_id = data_dict.get('user_id')
    post_id = data_dict.get("post")
    comment_str = data_dict.get("comment")
    parent_id = data_dict.get("parent_id")

    if not all([post_id, comment_str]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")

    try:
        post = Post.query.get(post_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not post:
        return jsonify(errno=RET.NODATA, errmsg="该新闻不存在")
    # 初始化模型，保存数据
    user = User.query.get(user_id)
    comment = Comment()
    comment.user_id = user.id
    comment.post_id = post_id
    comment.content = comment_str
    if parent_id:
        comment.parent_id = parent_id

    # 保存到数据库
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存评论数据失败")

    # 返回响应
    return jsonify(errno=RET.OK, errmsg="评论成功", data=comment.to_dict())
