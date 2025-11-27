

FROM python:3.10-slim-bookworm

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /app
WORKDIR /app
COPY . /app
EXPOSE 8080
CMD ["python", "bot.py"]
