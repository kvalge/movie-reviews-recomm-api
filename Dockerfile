FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
