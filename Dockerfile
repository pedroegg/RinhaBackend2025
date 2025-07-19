FROM python:3.11.2

ENV DEBIAN_FRONTEND=noninteractive

RUN ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone && \
    apt-get update && apt install -y tzdata

#RUN apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

WORKDIR /code
COPY app /code

ENV PATH="/rinha-backend-2025-venv/bin:${PATH}"

CMD ["uwsgi", "uwsgi.ini"]