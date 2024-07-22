import polars as pl
from datetime import time


def process_day(prices_for_day, threshold_move, sl, exit_time):
    try:
        exit_time = time(*exit_time)
        buy_trigger = pl.col("close") >= pl.col("close").first() * (1 + threshold_move)
        sell_trigger = pl.col("close") <= pl.col("close").first() * (1 - threshold_move)

        # Adding triggers to the dataframe
        prices_for_day = prices_for_day.with_columns(
            trigger=pl.when(buy_trigger)
            .then(1)
            .when(sell_trigger)
            .then(-1)
            .otherwise(0)
        )

        schema = prices_for_day.schema

        trades = []

        def get_entry_exit(prices_for_day) -> None:

            if len(prices_for_day) < 2:
                return

            if all(prices_for_day["trigger"] == 0):
                return

            # Getting the entry info
            entry_info = prices_for_day.filter(pl.col("trigger") != 0)[0]

            buy_exit = (pl.col("close") <= entry_info["close"] * (1 - sl)) | (
                pl.col("timestamp").dt.time() >= exit_time
            )
            sell_exit = (pl.col("close") >= entry_info["close"] * (1 + sl)) | (
                pl.col("timestamp").dt.time() >= exit_time
            )
            # Getting the exit info
            remaining_day = prices_for_day.filter(
                pl.col("timestamp") > entry_info["timestamp"]
            )

            exit_info = remaining_day.filter(
                buy_exit if entry_info["trigger"][0] == 1 else sell_exit
            )[0].with_columns(trigger=(-1 * entry_info["trigger"]))

            # Filtering the day to only include rows after the exit to be passed to the next function call iteratively
            remaining_day = remaining_day.filter(
                pl.col("timestamp") >= exit_info["timestamp"]
            )

            trades.extend([entry_info, exit_info])

            get_entry_exit(remaining_day)

        get_entry_exit(prices_for_day)

        if len(trades) == 0:
            return pl.DataFrame(schema=schema)

        return pl.concat(trades).sort("timestamp")
    except Exception as e:
        print(f"Failed for day {prices_for_day['timestamp'][0]} with error {e}")
        return pl.DataFrame(schema=schema)
