FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a non-root user and give them ownership of the app directory
RUN useradd -m ctfuser
RUN chown -R ctfuser:ctfuser /app

# Switch to the non-root user
USER ctfuser

EXPOSE 1337

CMD ["python", "app.py"]
