FROM python:3.7-slim

RUN mkdir /app
COPY /requirements.txt /app
RUN pip install -r /app/requirements.txt --no-cache-dir
COPY .. /app
WORKDIR /app

#CMD ["python3", "manage.py", "runserver", "0:8000"]
CMD ["gunicorn", "book_library.wsgi:application", "--bind", "0:8000" ]