FROM python:3.10.8-alpine

WORKDIR /usr/src/app

RUN apk update && apk upgrade
RUN apk add --no-cache gcc libc-dev

RUN python -m pip install --upgrade pip

COPY ./emulator/requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

CMD python start_emulating.py