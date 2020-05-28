from flask import current_app, abort, render_template, request, jsonify

from blog import db
from blog.models import Post, Category, Comment
from blog.modules.detail import detail_bp
from blog.utils.response_code import RET


@detail_bp.route('/<int:post_id>')
def post_detail(post_id):
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

    post.clicks += 1
    try:
        comments = Comment.query.filter(Comment.post_id == post_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
        abort(404)
    comment_list = []
    for comment in comments:
        comment_list.append(comment.to_dict())

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库操作失败")

    data = {
        "post": post.to_dict(),
        'category_list': category_list,
        'comment_list': comment_list
    }

    return render_template('blog/details.html', data=data)


@detail_bp.route('/like', methods=["POST"])
def post_add_like():
    post_id = request.json.get("id")

    if not post_id:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        post_id = int(post_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        post = Post.query.get(post_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if not post:
        return jsonify(errno=RET.NODATA, errmsg="评论不存在")

    post.likes += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库操作失败")

    return jsonify(errno=RET.OK, errmsg="OK")
