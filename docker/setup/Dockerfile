FROM python:3.11.2 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone && \
    apt-get update && apt install -y tzdata

RUN apt-get install -y --no-install-recommends \
    make build-essential gcc libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev \
    libxmlsec1-dev libffi-dev liblzma-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY app/requirements.txt .
RUN python -m venv /rinha-backend-2025-venv \
    && /rinha-backend-2025-venv/bin/pip install --upgrade pip setuptools \
    && /rinha-backend-2025-venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.11.2 AS runtime

WORKDIR /code
COPY --from=builder /rinha-backend-2025-venv /rinha-backend-2025-venv
ENV PATH="/rinha-backend-2025-venv/bin:$PATH"

COPY app /code
CMD ["python", "setup/main.py"]