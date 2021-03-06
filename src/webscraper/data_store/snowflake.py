import time
import pandas as pd

from sqlalchemy import create_engine

from src.webscraper.data_store.aws_config import secret_extraction as se


def _sql_alchemy_connect():
    engine = create_engine(
        "snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}"
        "&role={role}".format(
            user="PROSPECTOR_LIVE",
            password=se.config_secret("dummy_secret"),
            account="simplybusiness.eu-west-1",
            warehouse="transforming",
            role="TRANSFORMER",
            database="LIVE_PRODUCTION",
            schema="EVENTS",
        )
    )
    return engine


def input_df_to_db(df, table):
    start_time = time.time()
    db = _sql_alchemy_connect()
    df.to_sql(table, con=db, if_exists="append")
    print("--- %s seconds ---" % (time.time() - start_time))


def execute_query_with_output(sql_query_file):
    """
    Executes SQL query that produces output. E.g.: `SELECT GETDATE()`
    :param sql_query_file: an SQL query file to execute
    :return: result of the query
    """
    db = _sql_alchemy_connect()

    with open(f"queries/{sql_query_file}", "r") as query:
        df = pd.read_sql_query(query.read(), db)
        query.close()
    return df
