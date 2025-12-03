

FROM python:3.10-slim-bookworm

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt

RUN useradd -m -u 1000 user

WORKDIR /app
COPY . /app

RUN chown -R user:user /app && chmod -R 755 /app

USER user

EXPOSE 8080
CMD ["python", "bot.py"]
