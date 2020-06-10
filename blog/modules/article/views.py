from flask import current_app, render_template, request, jsonify, abort

from . import article_bp
from blog.models import Post, Category, Comment
from blog import constants
from ...utils.response_code import RET


@article_bp.route('/<int:post_id>')
def post_detail(post_id):
    """
    博文详情
    :param post_id:
    :return:
    """

    try:
        post = Post.query.get(post_id)
    except Exception as e:
        current_app.logger.error(e)

    if not post:
        abort(404)

    post.clicks += 1

    comments = []
    try:
        comments = Comment.query.filter(Comment.news_id == post_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)

    comment_dict_li = []
    for comment in comments:
        comment_dict = comment.to_dict()
        comment_dict_li.append(comment_dict)

    data = {
        "news": post.to_dict(),
        "comments": comment_dict_li
    }
    return render_template("blog/read.html", data=data)


@article_bp.route('/')
def article_index():
    post_list = None
    try:
        post_list = Post.query.order_by(Post.clicks.desc()).limit(constants.CLICK_RANK_MAX_POST)
    except Exception as e:
        current_app.logger.error(e)
    post_dict_list = []
    for post in post_list:
        post_dict_list.append(post.to_basic_dict())

    categories = Category.query.all()
    category_list = []

    for category in categories:
        category_list.append(category.to_dict())

    tops = Post.query.filter(Post.is_top == 0)
    top_list = []
    for top in tops:
        top_list.append(top.to_review_dict())
    data = {
        'post_dict_list': post_dict_list,
        'category_list': category_list,
        'top_list': top_list
    }
    return render_template('blog/article.html', data=data)


@article_bp.route('/post_list')
def post_list():
    # 1. 取到请求参数
    cid = request.args.get("cid", "1")
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", 1)
    try:
        page = int(page)
        cid = int(cid)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数")

    filters = [Post.status == 0]
    if cid != 1:
        filters.append(Post.category_id == cid)
    try:
        paginate = Post.query.filter(*filters).order_by(Post.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    post_model_list = paginate.items
    total_page = paginate.pages
    current_page = paginate.page

    post_dict_li = []
    for post in post_model_list:
        post_dict_li.append(post.to_basic_dict())

    data = {
        "current_page": current_page,
        "post_dict_li": post_dict_li,
        "pages": total_page
    }
    return jsonify(errno=RET.OK, errmsg="OK", data=data)
