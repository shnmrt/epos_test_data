import pandas as pd 
import numpy as np 
import random

def gen_random_datetimes(start:str, end:str, count:int) -> pd.DatetimeIndex:
    start_ts = pd.Timestamp(start).value
    end_ts = pd.Timestamp(end).value 

    random_ts = np.random.randint(start_ts, end_ts, size=count)

    return pd.to_datetime(random_ts).as_unit("us")

data_ranges = [
    ("2024-01-01", "2024-12-31", 100_000),  
    ("2025-01-01", "2025-12-31", 500_000)
]

for dr in data_ranges:
    dates = gen_random_datetimes(dr[0], dr[1], dr[2])
    vals_temp = [random.uniform(60,80) for _ in range(dr[2])]
    vals_pres = [random.uniform(1,5) for _ in range(dr[2])]
    
    df_temp = pd.DataFrame({"Datetime": dates.sort_values(), "Temperature": vals_temp})
    df_pres = pd.DataFrame({"Datetime": dates.sort_values(), "Pressure": vals_pres})

    df_temp.to_parquet(
        f"temp_{''.join(dr[0].split('-'))}_{''.join(dr[1].split('-'))}.parquet",
        row_group_size=10_000,
        write_statistics=True,
        compression="zstd"
    )

    df_pres.to_parquet(
        f"press_{''.join(dr[0].split('-'))}_{''.join(dr[1].split('-'))}.parquet",
        row_group_size=10_000,
        write_statistics=True,
        compression="zstd"
        )