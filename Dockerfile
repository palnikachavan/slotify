FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt


ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]