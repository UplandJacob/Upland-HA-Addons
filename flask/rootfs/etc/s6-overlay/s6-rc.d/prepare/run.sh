#!/usr/bin/with-contenv bashio

set -euo pipefail

if [ ! -d /config ]; then
    bashio::log.green "Creating '/config' folder..."
    mkdir /config
fi

if [ ! -d /config/flask ]; then
    bashio::log.green "Creating folder 'flask' in '/config'..."
    mkdir -p /config/flask
fi

if [ ! -f /config/flask/requirements.txt ]; then
    bashio::log.green "Copying default 'requirements.txt' to '/config/flask'..."
    cp /default_config/requirements.txt /config/flask/requirements.txt
fi

if [ ! -d /config/flask/.venv ]; then
    bashio::log.green "Creating virtual environment in '/config/flask'..."
    python3 -m venv /config/flask/.venv
fi
# Activate the virtual environment
bashio::log.green "Activating virtual environment in '/config/flask' (.venv)..."
source /config/flask/.venv/bin/activate

# Install the required packages from the user's requirements.txt
bashio::log.green "Installing required packages from '/config/flask/requirements.txt'"
python3 -m pip install --no-cache-dir --break-system-packages -r /config/flask/requirements.txt

if [ ! -f /config/flask/main.py ]; then
    bashio::log.green "Copying default 'main.py' to '/config/flask'"
    cp /default_config/main.py /config/flask/main.py
fi

bashio::log.green "Finished preparing Flask application"
