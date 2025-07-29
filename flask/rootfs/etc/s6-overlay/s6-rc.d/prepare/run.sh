#!/usr/bin/with-contenv bashio

if [ ! -f /config/requirements.txt ]; then
    bashio::log.green "Copying default requirements.txt to /config"
    cp /default_config/requirements.txt /config/requirements.txt
fi

if [ ! -d /config/flask ]; then
    bashio::log.green "Creating folder 'flask' in /config"
    mkdir -p /config/flask
fi
if [ ! -d /config/flask/bin ]; then
    bashio::log.green "Creating virtual environment in /config/flask"
    python3 -m venv /config/flask
fi
# Activate the virtual environment
bashio::log.green "Activating virtual environment in /config/flask"
source /config/flask/bin/activate

# Install the required packages from the user's requirements.txt
bashio::log.green "Installing required packages from /config/requirements.txt"
python3 -m pip install --no-cache-dir --break-system-packages -r /config/requirements.txt

if [ ! -f /config/flask/main.py ]; then
    bashio::log.green "Copying default main.py to /config/flask"
    cp /default_config/main.py /config/flask/main.py
fi