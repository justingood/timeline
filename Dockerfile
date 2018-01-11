FROM python:3-alpine

RUN mkdir -p /app/db
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app/
COPY templates/* templates/

EXPOSE 5000

CMD ["python", "main.py"]
