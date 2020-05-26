from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from portfolio.extensions import db
from portfolio.models import Essay
from portfolio.writings.forms import EssayForm
from flask_login import login_required

writings_blueprint = Blueprint('writings', __name__, template_folder = 'templates/writings')


@writings_blueprint.route('/post', methods = ['GET', 'POST'])
@login_required
def post_essay():
    form = EssayForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        new_essay = Essay(title, text)
        db.session.add(new_essay)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post_essay.html', form = form)

@writings_blueprint.route('/<int:essay_id>')
def essay_detail(essay_id):
    essay = Essay.query.get_or_404(essay_id)
    return render_template('essay_detail.html' , essay = essay)


@writings_blueprint.route('/<int:essay_id>/update', methods = ['GET', 'POST'])
@login_required
def essay_update(essay_id):
    essay = Essay.query.get_or_404(essay_id)
    form = EssayForm()
    if form.validate_on_submit():
        essay.title = form.title.data
        essay.text = form.text.data
        db.session.commit()
        return redirect(url_for('writings.essay_detail', essay_id = essay_id))
    elif request.method == 'GET':
        form.title.data = essay.title
        form.text.data = essay.text
    return render_template('post_essay.html', title = 'Updating Essay', form = form)


@writings_blueprint.route('/<int:essay_id>/delete', methods = ['GET', 'POST'])
@login_required
def essay_delete(essay_id):
    essay = Essay.query.get_or_404(essay_id)
    db.session.delete(essay)
    db.session.commit()
    return redirect(url_for('index'))
