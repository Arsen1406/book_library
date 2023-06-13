FROM python:3.7-slim

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY book_library/ .

CMD ["gunicorn", "book_library.wsgi:application", "--bind", "0:8000" ]