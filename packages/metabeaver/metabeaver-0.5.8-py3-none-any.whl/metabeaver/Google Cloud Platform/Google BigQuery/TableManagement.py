from typing import List
import pandas as pd
import numpy as np
from google.cloud import bigquery


def create_bigquery_table(project_id, tableset, table_name, schema):
    """Creates a BigQuery table in the specified tableset with the given table name and schema.

    Args:
        project_id (str): The project ID for the BigQuery table.
        tableset (str): The tableset to create the table in.
        table_name (str): The name for the new BigQuery table.
        schema (list[google.cloud.bigquery.SchemaField]): The schema for the new BigQuery table.

    Returns:
        google.cloud.bigquery.table.Table: The newly created BigQuery table.
    """
    # Create the BigQuery client
    client = bigquery.Client(project=project_id)

    # Get a reference to the table
    table_ref = client.dataset(tableset).table(table_name)

    # Create the table object
    table = bigquery.Table(table_ref, schema=schema)

    # Create the table in BigQuery
    table = client.create_table(table)

    # Return the new table object
    return table


def create_schema(items: List, field_names: List[str]) -> List[bigquery.SchemaField]:
    """
    Creates a BigQuery schema based on a list of items.

    :param items: List of items to determine schema from.
    :param field_names: List of field names for each item in the list.
                        If not specified, default names are used.
    :return: List of BigQuery schema fields.
    """
    # Define a mapping between Python and BigQuery types
    type_map = {
        int: 'INTEGER',
        float: 'FLOAT',
        str: 'STRING',
        bool: 'BOOLEAN',
        bytes: 'BYTES',
        bytearray: 'BYTES',
        memoryview: 'BYTES',
        'Int64': 'INTEGER',
        'Float64': 'FLOAT',
        pd.Timestamp: 'TIMESTAMP',
        pd.DateOffset: 'DATE',
        pd.Timedelta: 'TIME',
        np.float16: 'FLOAT',
        np.float32: 'FLOAT',
        np.float64: 'FLOAT',
        np.int8: 'INTEGER',
        np.int16: 'INTEGER',
        np.int32: 'INTEGER',
        np.int64: 'INTEGER',
        np.uint8: 'INTEGER',
        np.uint16: 'INTEGER',
        np.uint32: 'INTEGER',
        np.uint64: 'INTEGER',
    }

    # Create an empty list to hold the schema fields
    schema = []

    # Iterate over each item in the list
    for idx, item in enumerate(items):
        # Get the type of the current item
        field_type = type(item)
        # Look up the corresponding BigQuery type in the type map
        bq_type = type_map.get(field_type, 'STRING')
        # Get the field name for the current item
        field_name = field_names[idx] if idx < len(field_names) else f'field_{idx}'
        # Create a new schema field with the determined type and name
        schema.append(bigquery.SchemaField(name=field_name, field_type=bq_type))

    return schema
