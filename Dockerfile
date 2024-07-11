# Use an official Python runtime as a parent image
FROM python:3.11
# Set the working directory
WORKDIR /labpal_gpt/

# Copy the current directory contents into the container at /app
COPY . /labpal_gpt/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3500
ENV FLASK_APP=labpal_chat_api.py

# Run app.py when the container launches
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:3500", "labpal_chat_api:app"]
