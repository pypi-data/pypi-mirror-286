# -*- coding: utf-8 -*-
import logging

import pandas as pd
from dagster import ConfigurableIOManager
from dagster import OpExecutionContext

class OxaigenDbIOManager(ConfigurableIOManager):
    """Oxaigen IOManager to handle loading the contents of tables as pandas DataFrames.

    Does not handle cases where data is written to different schemas for different outputs, and
    uses the name of the asset key as the table name.
    """

    con_string: str

    def handle_output(self, context: OpExecutionContext, obj):
        if isinstance(obj, pd.DataFrame):
            # write df to table
            asset_key = None
            if context is not None:
                try:
                    asset_key = context.asset_key.path[-1]
                except Exception as e:
                    print("NO ASSET KEY DEFINED, CANNOT UPLOAD TO DATABASE")
                    logging.error(e)
            if asset_key:
                print("PANDAS DATAFRAME IS BEING UPLOADED TO DATABASE!")
                obj.to_sql(name=asset_key, con=self.con_string, if_exists="replace")  # noqa
        elif obj is None:
            # dbt has already written the data to this table
            pass
        else:
            context.log.info(f"Unsupported object type {type(obj)} for DbIOManager, doing nothing.")
            pass

    def load_input(self, context) -> pd.DataFrame:
        """Load the contents of a table as a pandas DataFrame."""
        try:
            model_name = context.asset_key.path[-1]
            schema_name = context.asset_key.path[-2].lower()
            return pd.read_sql(f"""SELECT * FROM "{schema_name}"."{model_name}";""", con=self.con_string)
        except Exception as error:
            print(context)
            print(error)
