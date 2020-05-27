from flask import current_app, abort, render_template

from blog.models import Post, Category
from blog.modules.detail import detail_bp


@detail_bp.route('/<int:post_id>')
def post_detail(post_id):
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

    data = {
        "post": post.to_dict(),
        'category_list': category_list
    }
    return render_template('blog/details.html', data=data)


