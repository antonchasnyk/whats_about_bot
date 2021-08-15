from quart import Quart


app = Quart(__name__)


@app.route('/')
async def hello():
    return 'Hello world'

if __name__ == '__main__':
    app.run('127.0.0.1:500')
