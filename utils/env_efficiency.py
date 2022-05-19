import os
import fnmatch
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def fetch_env_efficiency_data():
   
    env_df = pd.read_csv(Path(f"data/env_efficiency.csv"), parse_dates=False)


    return env_df