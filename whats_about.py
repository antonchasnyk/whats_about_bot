from quart import Quart

app = Quart(__name__)


@app.route('/')
async def hello():
    return 'Hello word'

app.run()
