FROM python:3.11-alpine@sha256:4350f4caccd5f014eb107fd0c7348f428d6e9d9fb089797d6264a234592e0981 AS build

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk add --no-cache gcc musl-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine@sha256:4350f4caccd5f014eb107fd0c7348f428d6e9d9fb089797d6264a234592e0981

WORKDIR /home/django/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=build /opt/venv /opt/venv

RUN addgroup --system --gid 1001 django && \
    adduser --system --uid 1001 django && \
    mkdir -p /home/django/app/media/uploads && \
    chown -R django:django /home/django && \
    chmod -R 755 /home/django/app && \
    chmod 775 /home/django/app/media/uploads

COPY --chown=django:django . .

USER django

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]