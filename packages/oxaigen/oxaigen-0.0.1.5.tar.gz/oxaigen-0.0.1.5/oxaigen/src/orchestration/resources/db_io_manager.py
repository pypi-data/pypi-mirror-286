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

    def handle_output(self, context, obj):
        if isinstance(obj, pd.DataFrame):
            # write df to table
            asset_key = None
            schema_name = "public"
            if context is not None:
                try:
                    asset_key = context.asset_key.path[-1]
                    schema_name = context.asset_key.path[-2].lower()
                except Exception as e:
                    print("NO ASSET KEY DEFINED, CANNOT UPLOAD TO DATABASE")
                    logging.error(e)
                if asset_key:
                    obj.to_sql(name=asset_key, schema=schema_name, con=self.con_string,
                               if_exists="replace")  # noqa

    def load_input(self, context) -> pd.DataFrame:
        """Load the contents of a table as a pandas DataFrame."""
        try:
            model_name = context.asset_key.path[-1]
            schema_name = context.asset_key.path[-2].lower()
            return pd.read_sql(f"""SELECT * FROM "{schema_name}"."{model_name}";""", con=self.con_string)
        except Exception as error:
            print(context)
            print(error)
