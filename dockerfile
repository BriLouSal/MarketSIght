FROM python:3.11.5-slim-bookworm

RUN mkdir /app


WORKDIR /app



COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt /app/
 

COPY . .
# Expose Django URL
EXPOSE 8000
# And we run the django server after this
CMD python manage.py runserver [0.0.0.0:8000]



