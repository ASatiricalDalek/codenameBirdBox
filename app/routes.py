from app import app
from flask import render_template
from app import forms

# TODO: Figure out why puttng methods in the decorator breaks Docker container
@app.route('/', METHODS=['GET', 'POST'])
def startPage():
    login = forms.signIn()
    return render_template('login.html', form=login)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
