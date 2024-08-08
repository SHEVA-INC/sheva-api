FROM python:3.11-alpine@sha256:4350f4caccd5f014eb107fd0c7348f428d6e9d9fb089797d6264a234592e0981 as build

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

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
 
COPY --from=build /opt/venv /opt/venv
COPY . .

RUN addgroup --system --gid 1001 django && \
    adduser --system --uid 1001 django && \
    mkdir -p /app/media/uploads && \
    chmod -R 755 /app && \
    chmod -R 777 /app/media/uploads

RUN chown -R django:django /app && \
    chmod +x entrypoint.sh

USER django

EXPOSE 8000
ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
