# Use the official Python image based on Ubuntu
FROM python:3.11

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd

EXPOSE 8000
WORKDIR /anova_api
LABEL authors="anovaadm"

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# Set the entrypoint to run the Django application
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "anova_api.wsgi:application"]
