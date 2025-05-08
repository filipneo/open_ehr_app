FROM python:3.12-slim

WORKDIR /app

COPY requirements_docker.txt .
RUN pip install --no-cache-dir -r requirements_docker.txt

COPY . .

CMD ["python", "frontend_app.py"]
