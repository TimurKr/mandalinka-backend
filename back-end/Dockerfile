FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/mandalinka/back-end

COPY requirements.txt ./

RUN pip install --upgrade --root-user-action=ignore pip
RUN pip install --root-user-action=ignore -r requirements.txt

COPY . .
