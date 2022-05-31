from waitress import serve

import app

serve(app.app, port=8888, threads=1)
