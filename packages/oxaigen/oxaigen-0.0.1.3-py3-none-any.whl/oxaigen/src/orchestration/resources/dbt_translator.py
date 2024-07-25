# -*- coding: utf-8 -*-
from typing import Any, Mapping, Optional
from dagster_dbt import DagsterDbtTranslator
from dagster import AssetKey


class _TemplateDagsterDbtTranslator(DagsterDbtTranslator):
    """
    THIS CLASS MUST NEVER BE USED DIRECTLY!

    use create_custom_dbt_translator_class() instead as it also
    inserts the required get_asset_key() class method.
    """

    @classmethod
    def get_group_name(cls, dbt_resource_props: Mapping[str, Any]) -> Optional[str]:
        return "datawarehouse"

    @classmethod
    def get_metadata(cls, dbt_resource_props: Mapping[str, Any]) -> Mapping[str, Any]:
        """
        Custom function to set EXTRA metadata key-value pairs for a DBT asset
        """
        return {"Oxaigen": "DBT resource"}

    @classmethod
    def get_description(cls, dbt_resource_props: Mapping[str, Any]) -> str:
        """
        Custom function to set the description of the DBT asset which by default incudes the raw SQL code.
        This behaviour can be adapted below
        """
        custom_description = dbt_resource_props["name"] + "\n" + dbt_resource_props[
            "raw_code"]
        return custom_description


def create_oxaigen_dbt_translator_class(
        custom_prefix: str,
        source_tags_as_asset_prefix: bool = True,
        group_prefix: Optional[str] = None,
        source_group_prefix: Optional[str] = None
):
    class OxaigenDagsterDbtTranslator(_TemplateDagsterDbtTranslator):
        @classmethod
        def get_asset_key(cls, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
            asset_key = super().get_asset_key(dbt_resource_props)

            if group_prefix:
                asset_key = asset_key.with_prefix(group_prefix)

            if dbt_resource_props["resource_type"] == "source":

                if source_tags_as_asset_prefix:
                    dbt_tags = dbt_resource_props['tags']
                    if dbt_tags:
                        for item in dbt_tags:
                            asset_key = asset_key.with_prefix(item)

                if source_group_prefix:
                    asset_key = asset_key.with_prefix(source_group_prefix)

            else:
                if dbt_resource_props.get("alias"):
                    asset_key[0][-1] = dbt_resource_props["alias"]
                else:
                    last_string = asset_key[0][-1]
                    if last_string.startswith("prod_"):
                        last_string = last_string.replace("prod_", "", 1)
                    new_string = last_string.replace("_", " ").title().replace(" ", "")
                    asset_key[0][-1] = new_string
                asset_key = asset_key.with_prefix(f"{custom_prefix}")

            return asset_key

    return OxaigenDagsterDbtTranslator()
