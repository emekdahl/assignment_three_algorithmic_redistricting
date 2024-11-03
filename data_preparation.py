import io
import logging
import requests
import zipfile

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, LpStatus



logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def get_county_populations(filename):
    """Function that organizes county data into a more usable form."""

    try:
        df = pd.read_csv(filename)
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
    return merged_df


def redistrict_ohio(df: pd.DataFrame): 
    """In your wildest dreams."""

    num_districts = 16
    ideal_population = df['population'].sum() / num_districts
    min_pop, max_pop = 0.9 * ideal_population, 1.1 * ideal_population
    model = LpProblem("Ohio_Redistricting", LpMinimize)

    x = LpVariable.dicts("x", [(i, j) for i in df.index for j in range(num_districts)], 0, 1, LpBinary)

    for i in df.index:
        model += lpSum(x[(i, j)] for j in range(num_districts)) == 1

    population_deviation = LpVariable.dicts("deviation", range(num_districts), 0)

    for j in range(num_districts):
        district_population = lpSum(df.loc[i, 'population'] * x[(i, j)] for i in df.index)
        model += district_population <= ideal_population + population_deviation[j]
        model += district_population >= ideal_population - population_deviation[j]

    for idx, row in df.iterrows():
        county_id = row.name
        neighbors = [df[df['county_name'] == neighbor_name].index[0] 
                    for neighbor_dict in row['neighbors'] 
                    for neighbor_name in neighbor_dict.keys() 
                    if neighbor_name in df['county_name'].values]
        
        for j in range(num_districts):
            for neighbor_id in neighbors:
                model += x[(county_id, j)] <= x[(neighbor_id, j)]
                model += x[(neighbor_id, j)] <= x[(county_id, j)]

    model += lpSum(population_deviation[j] for j in range(num_districts))
    
    model.solve()
    logging.info(f"Optimization status: {LpStatus[model.status]}")

    assignments = {}
    for i in df.index:
        for j in range(num_districts):
            if x[(i, j)].varValue == 1:
                assignments[df.loc[i, 'county_name']] = j

    assignments_df = pd.DataFrame(list(assignments.items()), columns=['county_name', 'assigned_district'])
    assignments_df["county_name"] = assignments_df["county_name"].str.lower()
    return assignments_df


def get_county_map(assignments_df: pd.DataFrame):
    url = "https://www2.census.gov/geo/tiger/TIGER2024/COUNTY/tl_2024_us_county.zip"
    response = requests.get(url)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall("tl_2024_us_county")
    counties = gpd.read_file("tl_2024_us_county/tl_2024_us_county.shp")
    ohio_counties = counties[counties["STATEFP"] == "39"]
    ohio_counties["NAMELSAD"] = ohio_counties["NAMELSAD"].str.lower()
    merged = ohio_counties.merge(assignments_df, left_on="NAMELSAD", right_on="county_name")
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    merged.plot(column="assigned_district", cmap="tab20", legend=True, ax=ax)
    for idx, row in merged.iterrows():
        plt.annotate(
            text=row["assigned_district"],
            xy=(row.geometry.centroid.x, row.geometry.centroid.y),
            ha="center",
            fontsize=8,
            color="black"
        )
    ax.set_title("Ohio Counties with District Assignments")
    ax.axis("off")
    plt.savefig("ohio_district_map.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    logging.info("Map saved as 'ohio_district_map.png'.")



if __name__ == "__main__":
    df = get_county_populations('ohio_counties.csv')
    adj_df = process_adjacency_data('adjacent_counties.txt')
    working_df = join_pop_and_adjacency_dfs(df, adj_df)
    assigned_districts = redistrict_ohio(working_df)
    get_county_map(assigned_districts)