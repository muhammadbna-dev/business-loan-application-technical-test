FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app/backend
COPY requirements.txt /app/backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
