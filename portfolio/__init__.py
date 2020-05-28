import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import dash
import dash_bootstrap_components as dbc
from flask.helpers import get_root_path
from flask import render_template, request
from portfolio.models import Essay, Project

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    server = Flask(__name__)
    server.config['SECRET_KEY'] = '\xc1\x96[\x07a\xac\xbc.\xe5\xaf-\x13r\x05\x9a\x86;}I\xc6\xac\x80\xff^'
    server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from portfolio.covid19_search_engine.layout import layout as search_engine_layout
    from portfolio.covid19_search_engine.callbacks import register_callbacks as search_engine_register_callbacks

    from portfolio.covid19_sitrep.layout import layout as situation_layout
    from portfolio.covid19_sitrep.callbacks import register_callbacks as situation_register_callbacks

    register_dashapp(server, 'COVID19 Search Engine', 'covid19-search-engine', search_engine_layout, search_engine_register_callbacks)
    register_dashapp(server, 'COVID19 Situation', 'covid19-situation', situation_layout, situation_register_callbacks)

    register_extensions(server)
    register_blueprints(server)

    @server.route('/')
    def index():
        page = request.args.get('page', 1, type=int)
        essays = Essay.query.order_by(Essay.id.desc()).paginate(page=page, per_page=5)
        projects = Project.query.order_by(Project.id.desc()).paginate(page=page, per_page = 5)
        return render_template('index.html', essays = essays, projects = projects)

    @server.errorhandler(404)
    def page_not_found(e):
        return render_template('error_handler.html'), 404


    return server




def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=f'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + f'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport],
                           external_stylesheets=[dbc.themes.BOOTSTRAP])

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)


def register_extensions(server):
    from portfolio.extensions import db
    from portfolio.extensions import login_manager
    from portfolio.extensions import migrate

    db.init_app(server)
    login_manager.init_app(server)
    login_manager.login_view = 'login'
    migrate.init_app(server, db)


def register_blueprints(server):

    from portfolio.projects.views import projects_blueprint
    from portfolio.writings.views import writings_blueprint
    from portfolio.user.views import user_blueprint

    server.register_blueprint(projects_blueprint, url_prefix='/projects')
    server.register_blueprint(writings_blueprint, url_prefix='/writings')
    server.register_blueprint(user_blueprint, url_prefix='/user')
