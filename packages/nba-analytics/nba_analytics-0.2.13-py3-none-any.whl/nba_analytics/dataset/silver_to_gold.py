# Bussiness-Level Aggregates
# Deliver continuously updated, clean data to downstream users and apps

import numpy as np
import pandas as pd

from . import cleaning
from . import filtering

from ..utils import filename_grabber
from ..utils.config import settings
from ..utils.logger import get_logger


logger = get_logger(__name__)

FILTER_AMT = settings.FILTER_AMT


def create_overlap_data(df):
    """
    Creates a DataFrame of players who have played for more than 5 years.

    Args:
        df (pandas.DataFrame): The input DataFrame containing player statistics.

    Returns:
        numpy.array: The numpy array with player statistics for each 5 consecutive years a player plays.
    """
    logger.debug("Creating overlap data...")

    df_overlap = df.copy()

    # Convert DataFrame to numpy array
    np_overlap = df_overlap.to_numpy()

    # Get all unique slugs
    np_uniques = np.unique(np_overlap[:, 0])

    # Create a list of numpy arrays for each player
    np_overlap = [np_overlap[np_overlap[:, 0] == unique] for unique in np_uniques]

    # Create new numpy array
    np_out = []

    for player_stats in np_overlap:
        for i in range(len(player_stats) - 5):
            if player_stats[i][1] + 5 == player_stats[i + 5][1]:
                np_out.append(player_stats[i:i+5])

    # Convert list of numpy arrays to numpy array
    np_out = np.array(np_out)

    # Remove the slug column
    np_out = np_out[:, :, 1:]

    # Convert 3D numpy array to 2D numpy array
    np_out = np_out.reshape(np_out.shape[0], -1)

    return np_out


def create_gold_datasets(df):
    """
    Creates a dataset with player statistics for players who have played at least 5 years in the NBA.

    Args:
        df (pandas.DataFrame): The input dataframe containing player statistics.

    Returns:
        pandas.DataFrame: The filtered dataframe with player statistics for players who have played at least 5 years in the NBA.
        numpy.array: The numpy array with player statistics for each 5 consecutive years a player plays.
        dict: A dictionary where the key is the player's slug and the value is a list of the player's statistics.
    """
    logger.debug("Filtering dataset for players who have played for more than 5 years...")

    df_filtered = df.copy()
    
    df_overlap, df_first_five = filtering.filter_players_over_5_years(df_filtered)
    np_overlap = create_overlap_data(df_overlap)

    # Create a dictionary where the key is the slug and the value is the rows of the filtered dataset
    dict_df = df_filtered.groupby('slug').apply(lambda x: x.to_dict(orient='records'))

    return df_first_five, np_overlap, dict_df


def save_df_and_dict(df_tensor_ready, np_overlap, dict_df):
    """
    Saves the given DataFrame to a CSV file.

    Args:
        df_tensor_ready (pandas.DataFrame): The DataFrame to save.
        np_overlap (numpy.array): The numpy array to save.
        dict_df (dict): The dictionary to save.

    Returns:
        None
    """
    tensor_ready_path = filename_grabber.get_data_file('dataset', settings.DATA_FILE_5YEAR_TENSOR_NAME)
    overlap_path = filename_grabber.get_data_file('dataset', settings.DATA_FILE_5YEAR_OVERLAP)
    dict_path = filename_grabber.get_data_file('dataset', settings.DATA_FILE_5YEAR_JSON_NAME)

    logger.debug(f"Saving tensor_ready dataset to '{tensor_ready_path}'...")
    logger.debug(f"Saving overlap dataset to '{overlap_path}'...")

    # Save the filtered dataset and dictionary to a csv and json file
    df_tensor_ready.to_csv(tensor_ready_path, index=False)
    np.savez(overlap_path, np_overlap)
    dict_df.to_json(dict_path, indent=4)

    logger.debug(f"Tensor-ready dataset saved to: '{tensor_ready_path}'.")
    logger.debug(f"Overlap dataset saved to: '{overlap_path}'.")
    logger.debug(f"Filtered dictionary saved to: '{dict_path}'.")


def log_summary(df_first_five, np_overlap):
    """
    Prints a summary of the given DataFrame and its filtered version.

    Parameters:
    - df_first_five (pandas.DataFrame): The filtered DataFrame.
    - np_overlap (numpy.array): The numpy array with player statistics for each 5 consecutive years a player plays.

    Returns:
    None
    """
    logger.debug("Printing summary...")

    # Print the head of the filtered DataFrame
    logger.info(df_first_five.head())

    # Reshape the 2D numpy array to its original shape
    reshaped_overlap = np_overlap.reshape(np_overlap.shape[0], FILTER_AMT, -1)

    # Print the number of entries and the number of unique players in the filtered dataframe
    logger.info(f"Filtered DataFrame: Entries={len(df_first_five)}, Unique Players={len(df_first_five['slug'].unique())}")

    # Print the number of entries and the number of unique players in the overlap dataframe
    logger.info(f"Filtered DataFrame: Entries={reshaped_overlap.shape[0] * reshaped_overlap.shape[1]}, Unique Players={len(np_overlap)}")


def run_processing(df=None):
    # Load the data
    if df is None:
        df = pd.read_csv(filename_grabber.get_data_file("silver", settings.DATA_FILE_NAME))

    # Create a dataframe of players who have played for more than 5 years
    df_first_five, np_overlap, dict_df = create_gold_datasets(df)

    # Save the filtered dataframe and dictionary
    save_df_and_dict(df_first_five, np_overlap, dict_df)

    # Print a summary of the data
    log_summary(df_first_five, np_overlap)

    return df_first_five, np_overlap, dict_df


if __name__ == '__main__':
    run_processing()    