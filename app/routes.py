from app import app
from flask import render_template, flash, redirect, url_for, request, Response, Flask, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import forms, db, camera_pi, base_camera, route_logic, motor_pi
from app.forms import register
from app.models import users
from app.models import *


# Global variables to control the camera filter
# and whether the thread needs to be restarted
global filter
filter = 'colorswap'
global check
check = False


# The default page which will be rendered
@app.route('/')
def startPage():
    id = None
    if current_user.is_authenticated:
        id = current_user.get_id()
    return render_template('start.html', id=id)


# The page rendered for user login
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


# The page rendered after the user logs out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('startPage'))


# The page rendered when the user registers
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('startPage'))

    registrationForm = forms.register()
    if registrationForm.validate_on_submit():
        uname = registrationForm.username.data
        usr = users(username=uname)
        usr.set_password(registrationForm.password.data)
        db.session.add(usr)
        db.session.commit()
        committedUser = users.query.filter_by(username=uname).first()
        uid = committedUser.id
        attr = attributes(userID=uid, canFeed=1, canView=1, style='light')
        db.session.add(attr)
        db.session.commit()
        flash("User Registered")
        return redirect(url_for('login'))
    return render_template('register.html', form=registrationForm)


# The page rendered when the registered user clicks the view bird option
@app.route('/view/<username>', methods=['GET'])
@login_required
def birdView(username):
    can_feed = route_logic.canFeed(current_user.get_id())
    can_view = route_logic.canView(current_user.get_id())
    if request.method == "GET":
        # Allows authenticated user to view the stream
        usr = users.query.filter_by(username=username).first_or_404()
        return render_template('birdView.html', user=usr, can_feed=can_feed, can_view=can_view)
    if request.method == "POST":
        # Apply the selected filter and restart the stream
        global filter  # Indicates we are referring the the global filter
        filter = 'negative'
        global check  # Indicated we are referring the the global check
        check = True
        usr = users.query.filter_by(username=username).first_or_404()
        return render_template('birdView.html', user=usr, can_feed=can_feed, can_view=can_view)

    # Allows authenticated user to view the stream
    # usr = users.query.filter_by(username=username).first_or_404()
    # return render_template('birdView.html', user=usr, can_feed=can_feed, can_view=can_view)



@app.route('/birdstream')
def birdstream():
    # Handles the live stream to the img element on the live stream page
    return Response(route_logic.gen(camera_pi.Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Handles the jquery when pressing 'Feed' link/button on birdView.html
@app.route('/_feed')
def toFeed():
    # Call route logic to execute the motor spinning script
    route_logic.instant_feed(motor_pi.motor(), run=True)
    return ()

@login_required
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = forms.changeSettings()
    can_view = route_logic.canView(current_user.get_id())
    can_feed = route_logic.canFeed(current_user.get_id())
    if form.validate_on_submit():
        uid = current_user.get_id()
        attr = attributes.query.filter_by(userID=uid).first()
        if form.canFeed.data == 'True':
            attr.canFeed = 1
        else:
            attr.canFeed = 2

        if form.canView.data == 'True':
            attr.canView = 1
        else:
            attr.canView = 2

        attr.style = form.themes.data

        if form.scheduledFeed.data == True:
            attr.scheduleFeed = 1
        else:
            attr.scheduleFeed = 0

        feedDays = ""
        if form.feedDay_Monday.data:
            feedDays = feedDays + "M"
        if form.feedDay_Tuesday.data:
            feedDays = feedDays + "T"
        if form.feedDay_Wednesday.data:
            feedDays = feedDays + "W"
        if form.feedDay_Thursday.data:
            feedDays = feedDays + "R"
        if form.feedDay_Friday.data:
            feedDays = feedDays + "F"
        if form.feedDay_Saturday.data:
            feedDays = feedDays + "S"
        if form.feedDay_Sunday.data:
            feedDays = feedDays + "U"

        attr.feedDays = feedDays
        attr.feedHour = form.feedHour.data
        attr.feedMinute = form.feedMinute.data


        db.session.commit()
        flash("Settings updated")
        return render_template('settings.html', form=form, can_feed=can_feed, can_view=can_view)
    return render_template('settings.html', form=form, can_feed=can_feed, can_view=can_view)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
