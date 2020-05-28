from flask import request, jsonify, current_app, abort, render_template

from blog.models import Post, Comment, User, db, Category
from blog.modules.comment import comment_bp
from blog.utils.response_code import RET


@comment_bp.route('/add_comment', methods=["POST"])
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


@comment_bp.route('/<int:post_id>')
def post_comment(post_id):
    # 查询分类
    categories = Category.query.all()
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())

    try:
        post = Post.query.get(post_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    if not post:
        # 返回数据未找到的页面
        abort(404)

    data = {
        "post": post.to_dict(),
        'category_list': category_list,
        # 'comment_list': comment_list
    }
    return render_template('blog/comment.html', data=data)


@comment_bp.route('/like', methods=["POST"])
def comment_add_like():
    comment_id = request.json.get("id")

    if not comment_id:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        comment_id = int(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if not comment:
        return jsonify(errno=RET.NODATA, errmsg="评论不存在")

    comment.like_count += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库操作失败")

    return jsonify(errno=RET.OK, errmsg="OK")
