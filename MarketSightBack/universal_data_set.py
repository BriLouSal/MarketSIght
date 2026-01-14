import joblib

import json




from dotenv import load_dotenv


from MSOAI import (
    info_to_positivty_rating_positivety,
    info_to_positivty_rating_negative,
    info_to_positivty_rating_netural,
)

load_dotenv()




def generate_universal_dataset():
    """Generate one dataset for all stocks using fictional company data."""
    dataset = {
        "Positive": info_to_positivty_rating_positivety(),
        "Neutral":  info_to_positivty_rating_netural(),
        "Negative": info_to_positivty_rating_negative()
    }

    with open('sentiment_dataset_of_stocks.json', "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)


generate_universal_dataset()