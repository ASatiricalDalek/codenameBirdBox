from app import app


@app.route('/')
def hello_world():
    return 'Hello World! bitch'


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
