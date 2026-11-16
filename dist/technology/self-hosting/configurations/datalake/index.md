# Output Data Location
Source: https://docs.genguardx.ai/technology/self-hosting/configurations/datalake/
Markdown: https://docs.genguardx.ai/technology/self-hosting/configurations/datalake/index.md
Description: Configure OUTPUT_DATA_LOCATION so self-hosted GGX writes job results as Parquet files to a local folder or a mounted shared location.

When a job, such as a simulation, produces result tables, GGX writes them as Parquet files. The setting `OUTPUT_DATA_LOCATION` in `api_config.py` is the location pattern that these files are written to.

## Configuration

The pattern holds `{}`, which GGX replaces with the name of the result:

```python
OUTPUT_DATA_LOCATION = 'file:///opt/corridor/instances/default/data/results/{}.parquet'
```

Or, with an environment variable:

```sh
export CORRIDOR_OUTPUT_DATA_LOCATION='file:///opt/corridor/instances/default/data/results/{}.parquet'
```

If the location is a local path (it starts with `file://` or `/`), GGX creates the parent folder when it starts. The user that runs GGX must be able to write to it.

**Note**

In a multi-server or container deployment, the location must be a path that every GGX process that reads or writes results can reach, such as a shared volume. Containers run as UID 1001 and group 0, so the folder must be writable by group 0. See [Docker-Based GGX Deployment](https://docs.genguardx.ai/technology/self-hosting/installation/docker-based/#user-and-file-permissions).

## Data in other systems

Data that lives in an external system, such as a Parquet file in a cloud bucket, is registered as a dataset from the Datasets page. See the [Data Assets](https://docs.genguardx.ai/register-and-refine/inventory-management/table-registry/) documentation.
