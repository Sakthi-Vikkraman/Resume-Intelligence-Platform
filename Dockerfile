FROM python:3.10-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Install Node + npm
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

# Install frontend dependencies
WORKDIR /app/Client
RUN npm install

# Expose backend + frontend ports
EXPOSE 8000
EXPOSE 5173

# Return to base app directory
WORKDIR /app

# Start both servers (FastAPI + Vite dev)
CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & cd Client && npm run dev -- --host 0.0.0.0"]
