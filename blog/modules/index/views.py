from flask import render_template

from . import index_bp


@index_bp.route('/')
def index():
    return render_template('blog/index.html')


@index_bp.route('/article')
def article():
    return render_template('blog/article.html')



