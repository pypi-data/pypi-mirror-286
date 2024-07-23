import os
import time
import pandas as pd
from basketball_reference_web_scraper import client

from ..utils import filename_grabber
from ..utils.config import settings
from ..utils.logger import get_logger


# Data Creation Variables
BATCH_SIZE = 100
RETRY_DELAY = 60
YEARS_BACK = 12

logger = get_logger(__name__)


def create_directories():
    for directory in [filename_grabber.get_dataset_dir(), filename_grabber.get_logs_dir()]:
        os.makedirs(directory, exist_ok=True)
        if directory == settings.DATASET_DIR:
            for subdirectory in [settings.BRONZE_DIR, settings.SILVER_DIR, settings.GOLD_DIR]:
                os.makedirs(os.path.join(directory, subdirectory), exist_ok=True)

def update_players_csv(basic_file_name, advanced_file_name, year):
    players_basic_path = filename_grabber.get_data_file("bronze", basic_file_name)
    players_advanced_path = filename_grabber.get_data_file("bronze", advanced_file_name)

    players_data_basic = client.players_season_totals(season_end_year=year)
    players_data_advanced = client.players_advanced_season_totals(season_end_year=year)
    
    players_data_basic = pd.DataFrame(players_data_basic)
    players_data_advanced = pd.DataFrame(players_data_advanced)

    players_data_basic['Year'] = year
    players_data_advanced['Year'] = year
    
    if not os.path.exists(players_basic_path) or os.stat(players_basic_path).st_size == 0:
        logger.info(f"Generating new data for {basic_file_name} for year {year}")
        players_data_basic.to_csv(players_basic_path, index=False)
    else:
        logger.info(f"Appending new data to {basic_file_name} for year {year}")
        # Compare players_basic_path to players_data_basic and append data to file_df if the slug/year does not exist
        file_df = pd.read_csv(players_basic_path)
        for index, row in players_data_basic.iterrows():
            if not ((row['slug'] == file_df['slug']) & (row['Year'] == file_df['Year'])).any():
                file_df.loc[len(file_df)] = row
        file_df.to_csv(players_basic_path, index=False)
    
    if not os.path.exists(players_advanced_path) or os.stat(players_advanced_path).st_size == 0:
        logger.info(f"Generating new data for {advanced_file_name} for year {year}")
        players_data_advanced.to_csv(players_advanced_path, index=False)
    else:
        logger.info(f"Appending new data to {advanced_file_name} for year {year}")
        # Compare players_advanced_path to players_data_advanced and append data to file_df if the slug/year does not exist
        file_df = pd.read_csv(players_advanced_path)
        for index, row in players_data_advanced.iterrows():
            if not ((file_df['slug'] == row['slug']) & (file_df['Year'] == row['Year'])).any():
                file_df.loc[len(file_df)] = row
        file_df.to_csv(players_advanced_path, index=False)

    logger.info(f"Data saved to {players_basic_path} and {players_advanced_path} for year {year}")

def merge_player_data(basic_file_name, advanced_file_name, output_file_name):
    players_basic_path = filename_grabber.get_data_file("bronze", basic_file_name)
    players_advanced_path = filename_grabber.get_data_file("bronze", advanced_file_name)
    output_file_path = filename_grabber.get_data_file("bronze", output_file_name)

    players_basic_df = pd.read_csv(players_basic_path)
    players_advanced_df = pd.read_csv(players_advanced_path)

    merged_players_df = pd.concat([players_basic_df, players_advanced_df], axis=1)

    merged_players_df = merged_players_df.loc[:, ~merged_players_df.columns.duplicated()]

    merged_players_df.to_csv(output_file_path, index=False)

def collect_data():
    create_directories()

    for year in range(2001, 2025):
        update_players_csv(settings.PLAYERS_BASIC_NAME,
                           settings.PLAYERS_ADVANCED_NAME,
                           year)
        merge_player_data(settings.PLAYERS_BASIC_NAME,
                          settings.PLAYERS_ADVANCED_NAME,
                          settings.DATA_FILE_NAME)
        time.sleep(3.5) # Sleep for 3.5 seconds to avoid rate limiting

    logger.info("Data collection completed.")

if __name__ == '__main__':
    collect_data()
