import logging
import os
from flask import (
    send_from_directory,
    Flask,
    make_response,
    jsonify,
    render_template,
    request,
)
import webscraper

app_name = "prospect_webscraper"
logging.basicConfig(
    level=logging.DEBUG
    # ,format=f'%asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)  # initialise the python logger configs and default logging level to none
logger = logging.getLogger(app_name)  # creates the app logger
app = Flask(app_name)


# def process(file_name):
#     # do what you're doing
#     file_name = 'document_template.xltx'
#     wb = load_workbook('document.xlsx')
#     wb.save(file_name, as_template=True)
#
#     return send_from_directory(file_name, as_attachment=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/single_submission")
def single_submission():
    return render_template("single_submission.html")


@app.get("/multi_submission")
def multi_submission():
    return render_template("multi_submission.html")


@app.route("/api/single_submission/", methods=["GET"])
def single_api_submission():
    base_url = request.args.get("base_url")
    logging.info(f"Searching for {base_url}")
    output = jsonify(webscraper.single_site_scrape(base_url))
    return make_response(output, 200)


@app.get("/health")
def health():
    response = {"healthcheck": "I'm working here"}
    return make_response(jsonify(response), 200)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    app.run(port=8888, debug=True)
