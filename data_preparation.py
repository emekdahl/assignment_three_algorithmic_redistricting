import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def organize_data(filename):
    """Function that organizes county data into a more usable form."""

    try:
        df = pd.read_csv(filename)
        print(df)
        return df

    except Exception as e:
        logging.info(f"Something went wrong while importing the data: {e}")

if __name__ == "__main__":
    df = organize_data('ohio_counties.csv')