FROM python:3.12

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . .

EXPOSE 6000

CMD ["python", "main.py"]