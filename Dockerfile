# Use the official Airflow image
FROM apache/airflow:2.7.1-python3.8

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Install Playwright dependencies
RUN apt-get update && apt-get install -y \
    libgtk-3-0 libgbm-dev libx11-xcb1 libgdk-pixbuf2.0-0 \
    && apt-get clean

# Install Playwright
RUN python -m playwright install --with-deps

# Switch to Airflow user
USER airflow

# Set the working directory
WORKDIR /opt/airflow

# Set the entrypoint for Docker (Airflow scheduler, webserver, etc.)
ENTRYPOINT ["airflow", "webserver"]
