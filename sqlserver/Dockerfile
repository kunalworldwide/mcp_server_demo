FROM python:3.11-slim

# Install dependencies for pymssql
RUN apt-get update && apt-get install -y \
    build-essential \
    freetds-dev \
    freetds-bin \
    tdsodbc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the server script and requirements
COPY sql_server_mcp.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir pymssql mcp[cli] python-dotenv

# Create a .env file in the container
RUN touch .env

# Set the entrypoint
ENTRYPOINT ["python", "sql_server_mcp.py"]