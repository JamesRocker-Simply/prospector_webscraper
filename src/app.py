import logging
import os

from flask import (
    Flask,
    abort,
    after_this_request,
    current_app,
    jsonify,
    make_response,
    render_template,
    request,
    send_file,
    send_from_directory,
)

from webscraper.selenium_scrape import setup_webdriver, selenium_clean_up
from webscraper.webscraper import single_site_scrape, mass_webscrape
from webscraper.data_manipulation import file_management as fm

app_name = "prospect_webscraper"
logging.basicConfig(
    level=logging.INFO
    # ,format=f'%asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s' # customise the log formatting here
)  # initialise the python logger configs and default logging level to none
logger = logging.getLogger(app_name)  # creates the app logger
app = Flask(app_name)
app.config["UPLOAD_EXTENSIONS"] = [".csv", ".xls", ".xlsx"]


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
    selenium_driver = setup_webdriver()
    output = jsonify(single_site_scrape(base_url, selenium_driver))
    selenium_clean_up(selenium_driver)
    return make_response(output, 200)


@app.route("/upload", methods=["POST"])
def upload_file():
    # check if the post request has the file part
    uploaded_file = request.files["file"]
    file = uploaded_file.filename
    file_name = os.path.splitext(file)[0]
    if file != "":  # this is done on the renderer side too but just for precaution
        file_extension = os.path.splitext(file)[1]
        if file_extension not in current_app.config["UPLOAD_EXTENSIONS"]:
            abort(400)
        uploaded_file.save(file)
    df = fm.read_excel_get_url_series(file)
    # output = fm.data_dict_to_pandas(webscraper.dry_run(df))  # for testing, add this in and remove the mass webscrape
    os.remove(file)  # remove the uploaded file

    # do the scraping
    selenium_driver = setup_webdriver()
    output = fm.data_dict_to_pandas(mass_webscrape(df, selenium_driver))
    selenium_clean_up(selenium_driver)

    # generate the output
    file_to_download = f"output/{file_name}_output{file_extension}"
    fm.output_excel_file(
        f"{file_to_download}", output
    )  # generate the file for the user to download
    return render_template(
        "dataframe_template.html",
        tables=output.to_html(),
        titles=file_name,
        file_to_download=file_to_download,
    )


@app.route("/download/output/<file_to_download>", methods=["GET", "POST"])
def download_file(file_to_download):
    @after_this_request
    def remove_file(response):
        # FIXME: if the file isn't downloaded then this stays in the output folder
        try:
            os.remove(f"output/{file_to_download}")
        except Exception as e:
            app.logger.error("Error removing or closing downloaded file handle", e)
        return response

    try:
        path = f"output/{file_to_download}"
        return send_file(path, download_name=file_to_download, as_attachment=True)
    except FileNotFoundError:
        pass
        return """
        <html><body>
         I've seen data you people wouldn't believe... Unstructured data in production databases... I watched users abuse
         column typing using only varchar. Like the file you requested a second time, those moments will be lost in
          time, like tears in rain
          <br><a href="/">Go back to the home page</a></br>
        </body>       
        </html>
        """
    except Exception as error:
        return app.logger.error("Unable to serve the requested file", error)


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
