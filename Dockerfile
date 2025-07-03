FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "main.py"]
