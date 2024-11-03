import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def get_county_populations(filename):
    """Function that organizes county data into a more usable form."""

    try:
        df = pd.read_csv(filename)
        # print(df)
        return df

    except Exception as e:
        logging.info(f"Something went wrong while importing the population data: {e}")


def process_adjacency_data(file_path):
    """Reads a JSON file and processes Ohio county adjacency data, including multiple neighbors."""
    
    df = pd.read_json("adjacent_counties.json")
    return df
    print(df.head())


def join_pop_and_adjacency_dfs(population_df: pd.DataFrame, adjacency_df: pd.DataFrame) -> pd.DataFrame:
    """tada"""

    population_df['county_name'] = population_df['county_name'].str.lower()
    adjacency_df['county_name'] = adjacency_df['county_name'].str.lower()

    merged_df = pd.merge(population_df, adjacency_df, left_on='county_name', right_on='county_name', how='left')
    print(merged_df)

if __name__ == "__main__":
    df = get_county_populations('ohio_counties.csv')
    adj_df = process_adjacency_data('adjacent_counties.txt')
    working_df = join_pop_and_adjacency_dfs(df, adj_df)