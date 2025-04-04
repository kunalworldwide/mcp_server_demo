from typing import Any, Dict, List, Optional
import os
from dotenv import load_dotenv
import pymssql
from mcp.server.fastmcp import FastMCP
import json

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("sqlserver")

# Database connection parameters
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME", "TestDB")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Helper function to get database connection
def get_db_connection():
    # Parse server and port - SQL Server Docker uses hostname,port format
    server_parts = DB_SERVER.split(',')
    server = server_parts[0]
    port = server_parts[1] if len(server_parts) > 1 else DB_PORT
    
    return pymssql.connect(
        server=server,
        port=int(port),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Helper function to execute SQL queries
def execute_query(query, params=None, fetch=True):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = None
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.rowcount
            
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

# Tool implementations for CRUD operations
@mcp.tool()
async def create_table(table_name: str, schema: str) -> str:
    """Create a new table in the database.
    
    Args:
        table_name: Name of the table to create
        schema: SQL schema definition for the table
    """
    try:
        query = f"IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = '{table_name}') CREATE TABLE {table_name} ({schema})"
        execute_query(query, fetch=False)
        return f"Table '{table_name}' created successfully."
    except Exception as e:
        return f"Error creating table: {str(e)}"

@mcp.tool()
async def insert_data(table_name: str, data: str) -> str:
    """Insert data into a table.
    
    Args:
        table_name: Name of the table
        data: JSON string with column-value pairs for insertion
    """
    try:
        data_dict = json.loads(data)
        
        columns = ", ".join(data_dict.keys())
        placeholders = ", ".join(["%s" for _ in data_dict.keys()])
        values = list(data_dict.values())
        
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        result = execute_query(query, values, fetch=False)
        return f"Data inserted successfully. Rows affected: {result}"
    except Exception as e:
        return f"Error inserting data: {str(e)}"

@mcp.tool()
async def select_data(table_name: str, columns: Optional[str] = "*", condition: Optional[str] = None, limit: Optional[int] = 100) -> str:
    """Query data from a table.
    
    Args:
        table_name: Name of the table to query
        columns: Columns to return (default: all columns)
        condition: Optional WHERE clause
        limit: Maximum number of rows to return (default: 100)
    """
    try:
        query = f"SELECT TOP {limit} {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        
        result = execute_query(query)
        
        if isinstance(result, dict) and "error" in result:
            return f"Error querying data: {result['error']}"
        
        if not result:
            return f"No data found in table '{table_name}'."
        
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error querying data: {str(e)}"

@mcp.tool()
async def update_data(table_name: str, data: str, condition: str) -> str:
    """Update data in a table.
    
    Args:
        table_name: Name of the table
        data: JSON string with column-value pairs to update
        condition: WHERE clause to specify which rows to update
    """
    try:
        data_dict = json.loads(data)
        
        set_clause = ", ".join([f"{col} = %s" for col in data_dict.keys()])
        values = list(data_dict.values())
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        
        result = execute_query(query, values, fetch=False)
        return f"Data updated successfully. Rows affected: {result}"
    except Exception as e:
        return f"Error updating data: {str(e)}"

@mcp.tool()
async def delete_data(table_name: str, condition: str) -> str:
    """Delete data from a table.
    
    Args:
        table_name: Name of the table
        condition: WHERE clause to specify which rows to delete
    """
    try:
        query = f"DELETE FROM {table_name} WHERE {condition}"
        result = execute_query(query, fetch=False)
        return f"Data deleted successfully. Rows affected: {result}"
    except Exception as e:
        return f"Error deleting data: {str(e)}"

@mcp.tool()
async def list_tables() -> str:
    """List all tables in the database."""
    try:
        query = "SELECT name FROM sys.tables ORDER BY name"
        result = execute_query(query)
        
        if isinstance(result, dict) and "error" in result:
            return f"Error listing tables: {result['error']}"
        
        if not result:
            return "No tables found in the database."
        
        table_names = [row["name"] for row in result]
        return "Tables in database:\n" + "\n".join(table_names)
    except Exception as e:
        return f"Error listing tables: {str(e)}"

@mcp.tool()
async def describe_table(table_name: str) -> str:
    """Get the structure of a table.
    
    Args:
        table_name: Name of the table to describe
    """
    try:
        query = f"""
        SELECT 
            c.name as column_name,
            t.name as data_type,
            c.max_length,
            c.precision,
            c.scale,
            c.is_nullable,
            CASE WHEN pk.column_id IS NOT NULL THEN 1 ELSE 0 END AS is_primary_key
        FROM 
            sys.columns c
        JOIN 
            sys.types t ON c.user_type_id = t.user_type_id
        LEFT JOIN 
            (SELECT ic.column_id, ic.object_id
             FROM sys.index_columns ic
             JOIN sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id
             WHERE i.is_primary_key = 1) pk 
        ON 
            c.object_id = pk.object_id AND c.column_id = pk.column_id
        WHERE 
            c.object_id = OBJECT_ID('{table_name}')
        ORDER BY 
            c.column_id
        """
        
        result = execute_query(query)
        
        if isinstance(result, dict) and "error" in result:
            return f"Error describing table: {result['error']}"
        
        if not result:
            return f"Table '{table_name}' not found or has no columns."
        
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error describing table: {str(e)}"

@mcp.tool()
async def execute_custom_query(query: str, is_select: bool = True) -> str:
    """Execute a custom SQL query.
    
    Args:
        query: SQL query to execute
        is_select: True if this is a SELECT query, False for other query types
    """
    try:
        result = execute_query(query, fetch=is_select)
        
        if not is_select:
            return f"Query executed successfully. Rows affected: {result}"
        
        if isinstance(result, dict) and "error" in result:
            return f"Error executing query: {result['error']}"
        
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error executing query: {str(e)}"

@mcp.tool()
async def get_server_status() -> str:
    """Check the status of the SQL Server connection."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION as version")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        return f"""
SQL Server Status: Connected
Server Version: {version}

Connection Information:
- Server: {DB_SERVER}
- Database: {DB_NAME}
- Username: {DB_USER}
"""
    except Exception as e:
        return f"Error connecting to SQL Server: {str(e)}"

# Run the server
if __name__ == "__main__":
    print("Starting SQL Server MCP...")
    print(f"Connecting to: {DB_SERVER}, Database: {DB_NAME}")
    
    if not DB_PASSWORD:
        print("WARNING: No database password provided. Set the DB_PASSWORD environment variable.")
    
    # Initialize and run the server
    mcp.run(transport='stdio')