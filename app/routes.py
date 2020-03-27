from app import app
from flask import render_template, flash, redirect, url_for, request, Response, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import forms, camera_pi, route_logic, motor_pi, feed_obj
from app.models import *
from app.bb_log import bbLog
import random as r
''' Uses the same logging driver created in bbLog so that 
log file is consistent per session !!IMPORT THIS ANYWHERE LOGGING OCCURS'''

# Global variables to control the camera filter
# and whether the thread needs to be restarted
global filter
filter = 'none'
global check
check = False

# root of the app routes users either to the login page, if they're logged out, or the main page if they're logged in
@app.route('/')
def router():
    # If the user is logged in already, take them to the main page
    if current_user.is_authenticated:
        return redirect(url_for('startPage'))
    # if there are no administrators on the system, go to the out of box experience to create a new admin
    elif attributes.query.filter_by(isAdmin=1).first() is None:
        return redirect(url_for('oobe'))
    # Otherwise, redirect the user to the login page
    else:
        return redirect(url_for('login'))


@app.route('/oobe', methods=['GET', 'POST'])
def oobe():
    if current_user.is_authenticated:
        bbLog.info("Registration: " + str(current_user) + " has already successfully registered.")
        return redirect(url_for('startPage'))
    # Disallow access to the OOBE page if an admin already exists for security reasons
    if attributes.query.filter_by(isAdmin=1).first():
        bbLog.info("Out of Box Experience cannot be accessed if there is an existing administrator account")
        return redirect(url_for('login'))

    # Register a new user as administrator
    registrationForm = forms.register()
    if registrationForm.validate_on_submit():
        uname = registrationForm.username.data
        usr = users(username=uname)
        usr.set_password(registrationForm.password.data)
        usr.email = registrationForm.email.data
        db.session.add(usr)
        db.session.commit()
        committedUser = users.query.filter_by(username=uname).first()
        uid = committedUser.id
        attr = attributes(userID=uid, canFeed=1, style='light', isAdmin=1)
        db.session.add(attr)
        db.session.commit()
        flash("User Registered")
        bbLog.info("Registration: " + str(current_user) + " has successfully registered.")
        return redirect(url_for('login'))
    bbLog.info("Registration: Error occurred during first admin registration.")
    return render_template('oobe.html', form=registrationForm)


# The default page which will be rendered
@login_required
@app.route('/main', methods=['GET', 'POST'])
def startPage():
    if current_user.is_authenticated:
        theme = route_logic.get_user_theme()
        id = current_user.get_id()
        feed_times = route_logic.get_Feed_Schedule('all')
        attr = attributes.query.filter_by(userID=current_user.get_id()).first_or_404()
        can_feed = attr.check_feed()
        is_admin = attr.check_admin()
        times = feedTimes.query.filter_by().all()
        return render_template('start.html', id=id, feed_times=feed_times,
                           can_feed=can_feed, feeds=times, is_admin=is_admin, theme=theme)
    else:
        # if a user tries to navigate here without logging in via the URL, take them back to the login page
        return redirect(url_for('login'))
    id = None
    feed_times = route_logic.get_Feed_Schedule('all')
    attr = attributes.query.filter_by(userID=current_user.get_id()).first_or_404()
    can_feed = route_logic.convert_can_feed_from_db(attr.canFeed)
    times = feedTimes.query.filter_by().all()
    if current_user.is_authenticated:
        id = current_user.get_id()
    if request.method == "POST":
        return render_template('start.html', id=id, feed_times=feed_times, can_feed=can_feed, feeds=times)
    return render_template('start.html', id=id, feed_times=feed_times, can_feed=can_feed, feeds=times)


# The page rendered for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user somehow makes it to the login page without going through OOBE to make admin acct. Redirect them
    if attributes.query.filter_by(isAdmin=1).first():
        # if a logged in user tries to view the login page, send them home
        if current_user.is_authenticated:
            bbLog.info(("Login: "+str(current_user)+" is already logged in."))
            return redirect(url_for('startPage'))

        login = forms.signIn()
        # Only run this when the form is submitted, not on page load
        if login.validate_on_submit():
            # Query DB to get user
            usr = users.query.filter_by(username=login.username.data).first()
            if usr is None or not usr.check_password(login.password.data):
                flash("Incorrect Username or Password")
                bbLog.info("Login: User entered invalid credentials.")
                # Refresh page to show the flashed message
                return redirect(url_for('login'))
            login_user(usr, remember=login.remember.data)
            next_page = request.args.get('next')
            # 'next' will take the user to the last page they tried to visit before logging in
            # if that page required login and kicked them back to this page
            # .netloc ensures that the URL actually exists in the app and hasn't been injected
            if not next_page or url_parse(next_page).netloc != '':
                bbLog.info("Login: "+str(current_user)+" has logged in.")
                next_page = url_for('startPage')
            return redirect(next_page)
        return render_template('login.html', form=login)
    else:
        return redirect(url_for('oobe'))


# The page rendered after the user logs out
@app.route('/logout')
def logout():
    bbLog.info("Logout: " + str(current_user) + " has logged out.")
    logout_user()
    return redirect(url_for('login'))


# The page rendered when the user registers
@app.route('/register', methods=['GET', 'POST'])
def register():
    if attributes.query.filter_by(isAdmin=1).first():
        if current_user.is_authenticated:
            bbLog.info("Registration: " + str(current_user) + " has already successfully registered.")
            return redirect(url_for('startPage'))

        registrationForm = forms.register()
        if registrationForm.validate_on_submit():
            usr = users(username=registrationForm.username.data)
            usr.set_password(registrationForm.password.data)
            usr.email = registrationForm.email.data
            db.session.add(usr)
            db.session.commit()
            committedUser = users.query.filter_by(username=registrationForm.username.data).first()
            uid = committedUser.id
            attr = attributes(userID=uid, canFeed=1, style='light', isAdmin=0)
            db.session.add(attr)
            db.session.commit()
            flash("User Registered")
            bbLog.info("Registration: " + str(current_user) + " has successfully registered.")
            return redirect(url_for('login'))
        bbLog.info("Registration: Error occurred during registration.")
        return render_template('register.html', form=registrationForm)
    else:
        return redirect(url_for('oobe'))


@app.route('/birdstream')
def birdstream():
    # Handles the live stream to the img element on the live stream page
    return Response(route_logic.gen(camera_pi.Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Handles the jquery when pressing 'Feed' link/button on birdView.html
@app.route('/_feed')
def toFeed():
    # Call route logic to execute the motor spinning script
    route_logic.db_write_log(current_user.username, route_logic.write_time(), 'instant')
    route_logic.instant_feed(motor_pi.motor(), run=True)
    return jsonify() # return empty json since the function expects return, but don't need to give anything in this case


@login_required
@app.route('/schedule_settings', methods=['GET', 'POST'])
def schedule_settings():
    form = forms.feed_schedule()
    attr = attributes.query.filter_by(userID=current_user.get_id()).first_or_404()
    can_feed = attr.check_feed()
    is_admin = attr.check_admin()
    theme = route_logic.get_user_theme()
    # Ensure the user has permission to view this form
    if can_feed:
        # If the form passes validation and is submitted
        if form.scheduledFeed.data and form.validate_on_submit():
            # Get the current user's ID and load the attributes table for that usr (userID is FK with ID in users table)
            uid = current_user.get_id()
            attr = attributes.query.filter_by(userID=uid).first()

            # Set the attributes in the attributes table to the values in the form
            # Since SQLite does not have bools, some of this is passed to separate functions to convert bool to int
            attr.scheduleFeed = route_logic.convert_can_feed_from_form(form.scheduledFeed.data)
            attr.feedDays = route_logic.get_feed_days(
                form.feedDay_Monday.data,
                form.feedDay_Tuesday.data,
                form.feedDay_Wednesday.data,
                form.feedDay_Thursday.data,
                form.feedDay_Friday.data,
                form.feedDay_Saturday.data,
                form.feedDay_Sunday.data
            )
            attr.feedHour = form.feedHour.data
            attr.feedMinute = str(form.feedMinute.data)

            # write changes to DB and flash a message to users
            db.session.commit()
            flash("Schedule Updated")
            bbLog.info(str(current_user) + " successfully updated their scheduled feed.")
            return render_template('scheduledFeedSettings.html', form=form, can_feed=can_feed, is_admin=is_admin,
                                   theme=theme)

        # if the form validates but the "schedule feed" checkbox is unchecked, disable scheduled feeding
        elif form.validate_on_submit():
            attr.scheduleFeed = None
            attr.feedDays = None
            attr.feedHour = None
            attr.feedMinute = None
            flash('Scheduled feeding disabled')
            bbLog.info(str(current_user.username) + " disabled their scheduled feed")
            db.session.commit()

        if attr.scheduleFeed:
            # Auto populate form based on current settings
            bbLog.info("Populating " + current_user.username + " settings on feed schedule page")
            feeds = route_logic.get_Feed_Schedule(current_user.get_id())
            form.scheduledFeed.data = True
            if 'Mon' in feeds[0].feed_days:
                form.feedDay_Monday.data = True
            if 'Tues' in feeds[0].feed_days:
                form.feedDay_Tuesday.data = True
            if 'Wed' in feeds[0].feed_days:
                form.feedDay_Wednesday.data = True
            if 'Thur' in feeds[0].feed_days:
                form.feedDay_Thursday.data = True
            if 'Fri' in feeds[0].feed_days:
                form.feedDay_Friday.data = True
            if 'Sat' in feeds[0].feed_days:
                form.feedDay_Saturday.data = True
            if 'Sun' in feeds[0].feed_days:
                form.feedDay_Sunday.data = True
            form.feedHour.data = feeds[0].feed_hour
            form.feedMinute.data = feeds[0].feed_minute
    else:
        # users that are logged in but do not have rights to view this page (and have navigated directly via URL)
        # Are bounced back to the starting page.
        return redirect(url_for('startPage'))
    # If form fails to validate, reload the page (this could be a first time visit, no form submission attempted)
    return render_template('scheduledFeedSettings.html', form=form, can_feed=can_feed, is_admin=is_admin, theme=theme)


@login_required
@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    theme_form = forms.theme_settings()
    user_settings_form = forms.user_settings()
    attr = attributes.query.filter_by(userID=current_user.get_id()).first_or_404()
    usr = users.query.filter_by(id=current_user.get_id()).first()
    theme = route_logic.get_user_theme()
    # Tell the form what this user's current username and email are
    user_settings_form.existing_Email = usr.email
    user_settings_form.existing_Username = usr.username
    can_feed = attr.check_feed()
    is_admin = attr.check_admin()

    if user_settings_form.validate_on_submit():
        usr.email = user_settings_form.email.data
        usr.username = user_settings_form.username.data
        attr.style = user_settings_form.themes.data
        # Check if the user is trying to change their password or not
        if usr.check_password(user_settings_form.currentPassword.data) and user_settings_form.newPassword.data is not "":
            usr.set_password(user_settings_form.newPassword.data)
            flash("Password Updated")
            db.session.commit()
            return render_template('themeSettings.html', form=theme_form, can_feed=can_feed, is_admin=is_admin,
                                   user_settings_form=user_settings_form, theme=theme)
        elif usr.check_password(user_settings_form.currentPassword.data) == False and user_settings_form.newPassword.data is not "":
            flash('Current Password incorrect; password not updated')
            return render_template('themeSettings.html', form=theme_form, can_feed=can_feed, is_admin=is_admin,
                                   user_settings_form=user_settings_form, theme=theme)
        db.session.commit()
        flash("User settings updated!")
        # It's possible the user just changed the theme, so recheck the DB for any theme updates 
        theme = route_logic.get_user_theme()
        return render_template('themeSettings.html', form=theme_form, can_feed=can_feed, is_admin=is_admin,
                               user_settings_form=user_settings_form, theme=theme)

    # Pre-fill current settings
    user_settings_form.username.data = usr.username
    user_settings_form.email.data = usr.email
    user_settings_form.themes.data = attr.style
    return render_template('themeSettings.html', form=theme_form, can_feed=can_feed, is_admin=is_admin,
                           user_settings_form=user_settings_form, theme=theme)


@login_required
@app.route('/admin_settings', methods=['GET', 'POST'])
def admin_settings():
    theme = route_logic.get_user_theme()
    attr = attributes.query.filter_by(userID=current_user.get_id()).first_or_404()
    can_feed = attr.check_feed()
    is_admin = attr.check_admin()
    accounts = users.query.all()
    form = forms.admin_register()
    if form.validate_on_submit():
        usr = users(username=form.username.data)
        usr.set_password(form.password.data)
        usr.email = form.email.data
        db.session.add(usr)
        db.session.commit()
        committedUser = users.query.filter_by(username=form.username.data).first()
        uid = committedUser.id
        if form.isAdmin.data:
            isAdmin = 1
        else:
            isAdmin = 0
        attr = attributes(userID=uid, canFeed=1, style='light', isAdmin=isAdmin)
        db.session.add(attr)
        db.session.commit()
        flash("User Registered")
        bbLog.info("Registration: " + str(current_user) + " has successfully registered.")
        return redirect(url_for('admin_settings'))
    return render_template('adminSettings.html', accounts=accounts, can_feed=can_feed, is_admin=is_admin, form=form,
                           theme=theme)


@login_required
@app.route('/admin_users_settings/<uid>', methods=['GET', 'POST'])
def admin_users_settings(uid):
    theme = route_logic.get_user_theme()
    # Instantiate the form and determine the current user's access level
    form = forms.admin_settings()
    cur_attr = attributes.query.filter_by(userID=current_user.get_id()).first_or_404()
    can_feed = cur_attr.check_feed()
    is_admin = cur_attr.check_admin()
    # If the user is an administrator, allow them to continue. Otherwise, we kick them to the homepage
    if is_admin:
        user = users.query.filter_by(id=uid).first()
        attr = attributes.query.filter_by(userID=uid).first()
        # Get the selected user's current uname and email so the form will not fail validation
        # By default, uname and email must be unique, so submitting the form without changing the uname and email fails
        # By getting their existing uname and email, we can ensure the form submits (see forms.py for more)
        form.existing_Username = user.username
        form.existing_Email = user.email
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            attr.canFeed = route_logic.convert_can_feed_from_form(form.canFeed.data)
            # If the admin did not enter anything into the pw box, don't try and update the pw
            if form.newPassword.data is not "":
                user.set_password(form.newPassword.data)

            db.session.commit()
            flash(user.username + ' settings updated')
            return render_template('adminUserSettings.html',
                                   username=user.username, can_feed=can_feed, is_admin=is_admin, form=form, theme=theme)
        # If the user has permission to view this page, but has not submitted the form...
        # Pre-fill the form with the current settings of the user in question
        form.username.data = user.username
        form.email.data = user.email
        # Radio button values are True and False, but strings, not bools
        form.canFeed.data = str(attr.check_feed())
    else:
        # Kick non-admins who try and access this page via URL to the homepage
        return redirect(url_for('startPage'))
    return render_template('adminUserSettings.html',
                           username=user.username, can_feed=can_feed, is_admin=is_admin, form=form, theme=theme)


# Clear the feed log on the viewing page
@app.route('/_clearfeed')
def clear_feed():
    feedTimes.query.delete()
    db.session.commit()
    return jsonify()
