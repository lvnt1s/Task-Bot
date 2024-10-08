FROM python:latest

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "bot.py"]