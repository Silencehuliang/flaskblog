from flask import render_template

from apps.modules.index import index_bp


@index_bp.route('/')
def index():
    return render_template('blog/index.html')
