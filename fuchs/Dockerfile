FROM python:3

WORKDIR /usr/src/app

COPY fuchs/requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY fuchs .

EXPOSE 8000

CMD [ "fastapi", "run", "fuchs/main.py", "--proxy-headers", "--port", "8000" ]
