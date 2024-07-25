# Use the official Python slim image
FROM python:slim

# Set the working directory
WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy the current directory contents into the container at /app
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir hatchling build pytest

# build and install the project
RUN python -m build
RUN pip install --no-cache-dir dist/*.whl

# Command to run the Python script
CMD ["pytest", "-v", "tests/test_all.py"]
