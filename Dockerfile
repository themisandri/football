#Base image python
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN chmod +x ./run_app.sh

# entrypoint run the app
ENTRYPOINT ["./run_app.sh"]


