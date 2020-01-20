from app import app
from flask import render_template, flash, redirect, url_for
from app import forms


@app.route('/', methods=['GET', 'POST'])
def startPage():
    login = forms.signIn()
    # Only run this when the form is submitted, not on page load
    if login.validate_on_submit():
        flash('Login requested for user {}, remember={}'.format(login.username.data, login.remember.data))
        return redirect(url_for('startPage'))
    else:
        print(login.errors)
    return render_template('login.html', form=login)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
