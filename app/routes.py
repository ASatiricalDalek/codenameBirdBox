from app import app
from flask import render_template, flash, redirect, url_for, request, Response, Flask, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import forms, db, camera_pi, base_camera, route_logic, motor_pi
from app.forms import register
from app.models import users
import time



# emulated camera
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera


@app.route('/')
def startPage():
    return render_template('start.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if a logged in user tries to view the login page, send them home
    if current_user.is_authenticated:
        return redirect(url_for('startPage'))

    login = forms.signIn()
    # Only run this when the form is submitted, not on page load
    if login.validate_on_submit():
        # Query DB to get user
        usr = users.query.filter_by(username=login.username.data).first()
        if usr is None or not usr.check_password(login.password.data):
            flash("Incorrect Username or Password")
            # Refresh page to show the flashed message
            return redirect(url_for('login'))
        login_user(usr, remember=login.remember.data)
        next_page = request.args.get('next')
        # 'next' will take the user to the last page they tried to visit before logging in
        # if that page required login and kicked them back to this page
        # .netloc ensures that the URL actually exists in the app and hasn't been injected
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('startPage')
        return redirect(next_page)
    return render_template('login.html', form=login)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('startPage'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('startPage'))

    registrationForm = forms.register()
    if registrationForm.validate_on_submit():
        usr = users(username=registrationForm.username.data)
        usr.set_password(registrationForm.password.data)
        db.session.add(usr)
        db.session.commit()
        flash("User Registered")
        return redirect(url_for('login'))
    return render_template('register.html', form=registrationForm)


@app.route('/view/<username>', methods=['GET', 'POST'])
@login_required
def birdView(username):
    if request.method == "GET":
        # Allows authenticated user to view the stream
        usr = users.query.filter_by(username=username).first_or_404()
        return render_template('birdView.html', user=usr)
    if request.method == "POST":         
        run = True
        motor = motor_pi.motor()
        motor.spin(run)
        usr = users.query.filter_by(username=username).first_or_404()
        return render_template('birdView.html', user=usr)



@app.route('/birdstream')
def birdstream():
    # Handles the live stream to the img element on the live stream page
    return Response(route_logic.gen(camera_pi.Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/_feed')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
