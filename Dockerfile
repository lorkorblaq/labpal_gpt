# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to the root directory of the image
WORKDIR /

# Copy the entire labpal_gpt directory contents to the root directory
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 3500
EXPOSE 3500

# Run Gunicorn with Gevent
CMD ["gunicorn", "-w", "4", "-k", "gevent", "-b", "0.0.0.0:3500", "gpt:app"]
