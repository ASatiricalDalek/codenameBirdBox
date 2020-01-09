from app import app


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/test')
def test():
    return 'Hello Test!'


# if __name__ == '__main__':
 #   app.run(host='0.0.0.0')
