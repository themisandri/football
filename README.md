# Live Bet365 Football Data Bot

This is a Python bot made with Flask that gets live Bet365 data and sends notifications about interesting football matches. It uses the Bet365 API to retrieve data about football matches in real-time, and then it filters the matches based on certain criteria and sends notifications to the user about matches that meet those criteria.

# Getting Started
## Requirements
- Python 3.6 or higher
- Flask
- Requests
- Rapid API credentials

## Installation
1. Clone the repository to your local machine:
```bash
git clone https://github.com/themisandri/football.git
```
2. Install the required packages:
```bash
pip install flask requests
```
3. Set up your Bet365 API credentials.
4. Update the config.py file with your Bet365 API credentials.
5. Run the Flask app:
```bash
python app.py
```
# Install using Docker
## Prerequisites
Before installing the app, make sure that you have the following installed on your machine:

- Docker
- make

## Installation
1. Clone the repository to your local machine:
```bash
git clone https://github.com/themisandri/football.git
```
2. Navigate to the app directory:
```bash
cd repo-name/app-directory
```
3. Build the Docker image:
```bash
make build
```
4. Run the app using Docker:
```bash
make run
```

This will start the app in a Docker container and you can access it at http://localhost:5555.

# Configuration
The bot can be configured by editing the config.py file and adding the 'api_key' from Rapid API.

# Usage

Once the Flask app is running, the bot will start retrieving live football data from the Bet365 API. It will then filter the data based on the criteria specified in the config.py file.

When the bot finds a match that meets the criteria, it will send a notification to the user. The notification can be in the form of an email, a text message, or a push notification, depending on how you configure it.

# License

This project is licensed under the MIT License. See the LICENSE file for details.
