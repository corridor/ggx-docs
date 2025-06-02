# Datalake Integration

Corridor provides the ability to connect to different kinds of data lakes which could have data saved as `parquet`, `orc`,
`avro`, `hive tables` or any in any other format.

The user could define a custom file handler that would have the logic to read/write to/from the data lake.

## Example

The example focuses on creating a data source handler to read from hive tables.
The user needs to inherit the base class: `DataSourceHandler` and define the functions:

- `read_from_location`
- `write_to_location`

```python
from corridor_api.config.handlers import DataSourceHandler


class HiveTable(DataSourceHandler):
    """
    Consider a case where every data table is a table in the Hive metastore.
    The table `location` identifier is the table name.
    """

    name = 'hive'
    write_format = 'parquet'

    def read_from_location(self, location, nrow=None):
        try:
            import findspark

            findspark.init()
            import pyspark
        except ImportError:
            import pyspark

        spark = pyspark.sql.SparkSession.builder.getOrCreate()

        data = spark.table(location)
        if nrow is not None:
            data = data.limit(nrow)
        return data

    def write_to_location(self, data, location, mode='error'):
        return data.write.format(self.write_format).saveAsTable(location)
```

## Configuration

Once the handler class is created, it can be set up in `api_config.py` as below:
(assuming the handler is defined in a file called `hive_table_hander.py` alongside `api_config.py`)

```python
LAKE_DATA_SOURCE_HANDLER = 'hive_table_handler.HiveTable'
```
