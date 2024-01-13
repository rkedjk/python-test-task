FROM python:3.11.6-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app/
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the necessary files into the container
COPY app/geonames_db.py app/helpers.py app/__init__.py /app/app/
COPY databases/geonames_cities.sqlite databases/geonames.sqlite /app/databases/
COPY main.py /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

