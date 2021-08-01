FROM python:3.8-slim-buster
EXPOSE 6543
RUN mkdir /work
WORKDIR /work

RUN python3 -m pip install --upgrade pip==20.2

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src src

COPY setup.py ./
RUN pip install -e .

CMD ["python3", "src/flask_app.py"]