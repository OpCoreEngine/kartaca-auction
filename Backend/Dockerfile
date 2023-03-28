FROM python:3-alpine
WORKDIR /app
COPY ./requirements.txt /app
COPY ./app.py /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7003
CMD ["python", "app.py"]
