# SQL Server MCP

This project provides a Messaging Coordination Protocol (MCP) server that allows performing CRUD operations on a Microsoft SQL Server database.

## Prerequisites

- Docker installed
- SQL Server running in a Docker container (or elsewhere accessible)
- Docker Hub account (for publishing your image)

## Files

- `sql_server_mcp.py`: The MCP server implementation
- `requirements.txt`: Python dependencies
- `Dockerfile`: For building the Docker image
- `mcp_config.json`: Sample configuration for using the tool

## Building the Docker Image

1. Place all files in the same directory
2. Build the Docker image:

```bash
docker build -t your-docker-username/mcp-sql-server:latest .
```

3. Push the image to Docker Hub:

```bash
docker push your-docker-username/mcp-sql-server:latest
```

## Configuration

The MCP server requires these environment variables:

- `DB_SERVER`: SQL Server hostname and port (default: localhost,1433)
- `DB_NAME`: Database name (default: TestDB)
- `DB_USER`: SQL Server username (default: sa)
- `DB_PASSWORD`: SQL Server password

## Available Tools

The MCP server provides these tools for database operations:

1. `create_table`: Create a new table in the database
2. `insert_data`: Insert data into a table
3. `select_data`: Query data from a table
4. `update_data`: Update data in a table
5. `delete_data`: Delete data from a table
6. `list_tables`: List all tables in the database
7. `describe_table`: Get the structure of a table
8. `execute_custom_query`: Execute a custom SQL query
9. `get_server_status`: Check the status of the SQL Server connection

## Example Usage

Here are some examples of how to use the tools:

### Creating a Table

```
create_table table_name="Users" schema="ID int IDENTITY(1,1) PRIMARY KEY, Name varchar(100) NOT NULL, Email varchar(255) UNIQUE, CreatedDate datetime DEFAULT GETDATE()"
```

### Inserting Data

```
insert_data table_name="Users" data='{"Name": "John Doe", "Email": "john@example.com"}'
```

### Querying Data

```
select_data table_name="Users" columns="ID, Name, Email" condition="Name LIKE '%John%'" limit=10
```

### Updating Data

```
update_data table_name="Users" data='{"Name": "John Smith"}' condition="ID = 1"
```

### Deleting Data

```
delete_data table_name="Users" condition="ID = 1"
```

## Integration with Other MCPs

You can integrate this SQL Server MCP with other MCPs by modifying the `mcp_config.json` file.