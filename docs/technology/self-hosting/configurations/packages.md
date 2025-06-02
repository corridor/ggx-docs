# Additional Libraries

Corridor provides an option to allow the users to be able to use additional libraries which are not available
out of the box.

## Configuration

There are 5 steps which have to be followed so that the user is able to validate the definition
and run successful jobs on the platform.

1. Install the library in the virtual environment of API servers.
2. Install the library in the virtual environment of Worker-API servers.
3. Install the library in the virtual environment of Worker-Spark servers.
4. Install the library on the spark cluster.
5. Add the library to the Allowed Python Imports in the `Platform Settings` tab in the platform UI
