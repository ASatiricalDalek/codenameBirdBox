from app import app


@app.route('/')
def hello_world():
    return 'Hello World!'


# if __name__ == '__main__':
#     app.run(host='192.168.0.50')
