# This project involves developing a client-server script in Python that handles MQTT messages via RabbitMQ,
# processes these messages, stores them in MongoDB, and provides an endpoint to retrieve data based on a specified time range.

# The Structure of the project is as follows:

Project/
│
├── mqtt_client_file.py
├── mqtt_server_file.py
└── requirements.txt

git clone https://github.com/prasannadani9/UPSWING_MQTT.git

git checkout master

python -m venv projenv
.\projenv\Scripts\Activate.ps1

pip install -r requirements.txt

python mqtt_server_file.py

# In Another Terminal, do open client file

.\projenv\Scripts\Activate.ps1
python mqtt_client.py

# Ensure RabbitMQ and MongoDB are running before starting the scripts.

# API

# endpoint: POST /status
# request body

{
  "start_time": "2024-07-22T00:00:00",
  "end_time": "2024-07-22T23:59:59"
}

# response body

{
  "0": 15,
  "1": 20,
  "2": 10,
  "3": 5,
  "4": 8,
  "5": 12,
  "6": 9
}
