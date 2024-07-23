FROM python:3.10.12-slim-bookworm AS builder

RUN pip install hatch
COPY . /source
WORKDIR /source
RUN hatch build

FROM python:3.10.12-slim-bookworm

ENV PYCRDT_FLOW_LOG_LEVEL=INFO

RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /source/dist/*.whl /tmp/

RUN pip install --no-cache-dir $(echo /tmp/*.whl)[service]

ENTRYPOINT [ "tini", "--" ]

LABEL org.opencontainers.image.source https://github.com/Wh1isper/pycrdt-flow
