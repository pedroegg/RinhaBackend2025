FROM python:3.11.2

WORKDIR /code
COPY app /code

ENV PATH="/rinha-backend-2025-venv/bin:${PATH}"
CMD ["uwsgi", "uwsgi.ini"]