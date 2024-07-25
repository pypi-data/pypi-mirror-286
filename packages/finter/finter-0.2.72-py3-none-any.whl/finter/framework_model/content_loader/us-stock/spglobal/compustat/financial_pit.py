from datetime import datetime
from finter.calendar import iter_trading_days

import pandas as pd
from finter.framework_model.content import Loader

initial_date = 19820131


def safe_apply(x):
    if pd.isna(x):
        return x
    else:
        # key 값을 float으로 변환 가능한 경우에만 비교
        valid_items = {float(k): v for k, v in x.items() if is_float(k)}
        if valid_items:
            max_key = max(valid_items.keys())
            return valid_items[max_key]
        else:
            return None  # 모든 key가 float 변환 불가능한 경우


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class CompustatFinancialPitLoader(Loader):
    def __init__(self, cm_name):
        self.__CM_NAME = cm_name
        self.__FREQ = cm_name.split(".")[-1]

    @staticmethod
    def _unpivot_df(raw):
        unpivot_df = raw.unstack().dropna().reset_index()
        unpivot_df.columns = ["id", "pit", "val"]
        m = (
            pd.DataFrame([*unpivot_df["val"]], unpivot_df.index)
            .stack()
            .rename_axis([None, "fiscal"])
            .reset_index(1, name="value")
        )
        result = unpivot_df[["id", "pit"]].join(m)
        return result.dropna(subset=["fiscal", "value"])

    def get_df(
        self,
        start: int,
        end: int,
        fill_nan=True,
        mode: str = "default",
        *args,
        **kwargs
    ):
        """
        Fetch the financial data within a specified date range.

        Parameters
        ----------
        mode : str, optional
            Mode of data return. It can be one of the following:
            'default'  - Return the data with the safe apply function, which can be used directly after loading for modeling purposes (default behavior).
            'unpivot'  - Return the data in an unpivoted (long) format.
            'original' - Return the original raw data.

        Returns
        -------
        pandas.DataFrame
            The requested financial data in the specified format.

        Examples
        --------
        loader = CompustatFinancialPitLoader("some.cm.name")

        # Default data format
        df_default = loader.get_df(start=19820101, end=20230101, mode='default')

        # Unpivoted data format
        df_unpivot = loader.get_df(start=19820101, end=20230101, mode='unpivot')

        # Original raw data
        df_original = loader.get_df(start=19820101, end=20230101, mode='original')
        """
        assert mode in {
            "default",
            "unpivot",
            "original",
        }, "Mode must be one of 'default', 'unpivot', or 'original'."

        raw = self._load_cache(
            self.__CM_NAME,
            initial_date,
            end,
            freq=self.__FREQ,
            fill_nan=fill_nan,
            cache_t="hdf",
        ).dropna(how="all")

        raw = raw.dropna(how="all").loc[
            datetime.strptime(str(start), "%Y%m%d") : datetime.strptime(
                str(end), "%Y%m%d"
            )
        ]

        if mode == "unpivot":
            raw = CompustatFinancialPitLoader._unpivot_df(raw)
            return raw
        elif mode == "original":
            trading_dates = sorted(iter_trading_days(start, end, "us"))
            return raw.reindex(trading_dates)
        else:
            trading_dates = sorted(iter_trading_days(start, end, "us"))
            return raw.map(lambda x: safe_apply(x)).reindex(trading_dates)
