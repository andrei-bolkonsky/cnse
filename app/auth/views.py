from flask import render_template, session, flash, redirect, url_for, request
from . import auth
from .forms import LoginForm
from ..models import User
from flask_login import login_user, logout_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        form.username.data = ''
        user = User.query.filter_by(username=session['username']).first()
        if user is not None:
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
        flash("Nom d'utilisateur ou mot de passe invalide.")
    return render_template('auth/login.html',
                           form=form,
                           username=session.get('username'))

@auth.route('/logout')
def logout():
    logout_user()
    flash('Vous avez été déconnecté avec succès.')
    return redirect(url_for('main.index'))
