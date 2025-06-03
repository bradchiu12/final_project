FROM --platform=linux/amd64 python:3.14-rc-slim

WORKDIR /app

COPY requirements.txt /app/
COPY web2.py /app/
COPY templates /app/templates
COPY .env /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python", "web2.py"]

