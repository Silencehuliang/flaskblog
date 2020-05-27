from flask import current_app, render_template, request, jsonify

from blog import constants
from blog.models import Post, Category
from blog.modules.index import index_bp
from blog.utils.response_code import RET


@index_bp.route('/post_list')
def post_list():
    """
    首页博文数据
    :return:
    """
    # 获取当前页参数
    args_dict = request.args
    page = args_dict.get("p", "1")
    per_page = args_dict.get("per_page", constants.HOME_PAGE_MAX_POST)
    cid = args_dict.get("cid", '1')

    try:
        page = int(page)
        per_page = int(per_page)
        cid = int(cid)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数")

    filters = [Post.status == 0]
    # 3. 查询数据并分页
    if cid != 1:
        filters.append(Post.category_id == cid)
    try:
        paginate = Post.query.filter(*filters).order_by(Post.create_time.desc()).paginate(page, per_page, False)
        # 获取查询出来的数据
        post_model_list = paginate.items
        # 获取到总页数
        total_page = paginate.pages
        current_page = paginate.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    post_dict_list = []
    for post in post_model_list:
        post_dict_list.append(post.to_basic_dict())
    data = {
        "total_page": total_page,
        "current_page": current_page,
        "post_dict_list": post_dict_list
    }
    return jsonify(errno=RET.OK, errmsg="OK", data=data)


@index_bp.route('/')
def index():
    """
    首页
    :return:
    """
    categories = Category.query.all()
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())
    data = {
        'category_list': category_list
    }
    return render_template('blog/index.html', data=data)


