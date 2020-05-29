from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from portfolio.extensions import db
from portfolio.models import Project
from portfolio.projects.forms import ProjectForm
from flask_login import login_required

projects_blueprint = Blueprint('projects', __name__, template_folder = 'templates/projects')



@projects_blueprint.route('/post', methods = ['GET', 'POST'])
@login_required
def post_project():
    form = ProjectForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        image = form.image_url.data
        urlpath = form.urlpath.data
        new_project = Project(title, description, image, urlpath)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post_project.html', form = form)


@projects_blueprint.route('/<int:project_id>/update', methods = ['GET', 'POST'])
@login_required
def project_update(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.image = form.image_url.data
        project.urlpath = form.urlpath.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.image_url.data = project.image
        form.urlpath.data = project.urlpath
    return render_template('post_project.html', title = 'Updating Project', form = form)

@projects_blueprint.route('/<int:project_id>/delete', methods = ['GET', 'POST'])
@login_required
def project_delete(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))
