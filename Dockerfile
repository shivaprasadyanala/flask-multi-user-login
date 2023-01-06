FROM python:3.8
RUN mkdir /code
WORKDIR /code
COPY . .
COPY requirements.txt /code/
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "wsgi.py"]