FROM python:3.11
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app/

RUN apt-get update \
    && apt-get install -y netcat-traditional dos2unix \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/nc.traditional /usr/bin/nc

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN dos2unix /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]







