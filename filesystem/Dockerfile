FROM python:3.11-slim

WORKDIR /app

# Copy the server script
COPY filesystem_server.py /app/

COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory to mount host directories to
RUN mkdir -p /projects

# Set the entrypoint
ENTRYPOINT ["python", "filesystem_server.py"]

# Default command to allow directories under /projects
CMD ["/projects"]