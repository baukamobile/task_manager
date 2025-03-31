FROM python:3.12
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

ENV PYTHONUNBUFFERED=1
# COPY wait_for_db.py /app/
CMD ["sh", "-c", "python wait_for_db.py && gunicorn --bind 0.0.0.0:8000 --workers 3 taskmanager.wsgi:application"]

EXPOSE 8000
