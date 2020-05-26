#from portfolio import server
from flask import render_template, request
from portfolio.models import Essay, Project

from portfolio import create_app

server = create_app()

@server.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    essays = Essay.query.order_by(Essay.id.desc()).paginate(page=page, per_page=5)
    projects = Project.query.order_by(Project.id.desc()).paginate(page=page, per_page = 5)
    return render_template('index.html', essays = essays, projects = projects)

@server.errorhandler(404)
def page_not_found(e):
    return render_template('error_handler.html'), 404


if __name__ == '__main__':
    server.run(debug=True)
