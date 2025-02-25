# Use the official Python image based on Ubuntu
FROM python:3.11

# Set the author label
LABEL authors="anovaadm"

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint to run the Django application
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "anova_api.wsgi:application"]
