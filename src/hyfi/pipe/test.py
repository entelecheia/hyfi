import numpy as np
import pandas as pd


def preprocessing_esg_ratings(data: pd.DataFrame):
    # Define a mapping from ratings to numerical scores
    rating_map = {"A+": 6, "A": 5, "B+": 4, "B": 3, "C": 2, "D": 1, np.nan: np.nan}

    # Convert rating columns into numerical scores
    for year in range(2011, 2021):
        data[str(year)] = data[str(year)].map(rating_map)

    # Melt dataframe to have years as rows instead of columns
    melted_df = data.melt(
        id_vars=["type", "code", "name", "market"],
        var_name="year",
        value_name="rating_score",
        value_vars=[str(year) for year in range(2011, 2021)],
    )

    # Convert year to integer
    melted_df["year"] = melted_df["year"].astype(int)

    # Sort by type, code and year
    melted_df.sort_values(["type", "code", "year"], inplace=True)

    # Calculate rating change
    melted_df["rating_change"] = melted_df.groupby(["type", "code"])[
        "rating_score"
    ].diff()

    # Create 'rating' column by mapping numerical scores back to ratings
    reverse_rating_map = {v: k for k, v in rating_map.items()}
    melted_df["rating"] = melted_df["rating_score"].map(reverse_rating_map)

    # Set rating_change values to '1', '0', '-1' based on whether it's positive, zero or negative
    melted_df["rating_change"] = melted_df["rating_change"].apply(
        lambda x: 1 if x > 0 else (0 if x == 0 else (-1 if x < 0 else np.nan))
    )
    return melted_df
