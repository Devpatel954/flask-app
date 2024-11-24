from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Post

post = Blueprint('post', __name__)

@post.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', posts=posts)

@post.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post.dashboard'))
    return render_template('create_post.html')

@post.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.user_id != current_user.id:
        return 'Unauthorized', 403

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('post.dashboard'))
    return render_template('edit_post.html', post=post)

@post.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.user_id != current_user.id:
        return 'Unauthorized', 403

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('post.dashboard'))


