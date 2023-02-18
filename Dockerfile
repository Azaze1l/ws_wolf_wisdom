
FROM python:3.10-slim as builder
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc git build-essential
RUN pip install -U pip setuptools wheel

WORKDIR /wheels
COPY requirements.txt /
RUN pip wheel -r /requirements.txt


FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels
RUN apt update && apt install gettext -y
RUN pip install -U pip
RUN pip install /wheels/* \
        && rm -rf /wheels \
        && rm -rf /root/.cache/pip/*

WORKDIR /app
COPY . .
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["main.py"]
