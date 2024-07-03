FROM --platform=linux/x86_64 ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && \
    apt-get install -y \
    wget \
    xz-utils \
    bzip2 \
    git \
    python3-pip \
    python3 \
    && apt-get install -y software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt --break-system-packages

COPY filtered/ ./filtered/

CMD ["python3.11", "-m", "celery", "-A", "filtered.worker", "worker", "--loglevel=info", "--concurrency=1"]