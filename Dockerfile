FROM python:3.12-slim AS builder

ARG UV_VERSION=0.9.30
ENV UV_NO_CACHE=1
WORKDIR /build

RUN python -m pip install --no-cache-dir "uv==${UV_VERSION}"
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src/ src/
RUN uv build --wheel --out-dir /dist \
  && uv export --frozen --no-dev --no-emit-project \
    --no-hashes \
    --format requirements.txt \
    --output-file /dist/requirements.txt

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1
WORKDIR /app

RUN groupadd --system kicadmcp \
  && useradd --system --gid kicadmcp --home-dir /app --shell /usr/sbin/nologin kicadmcp

COPY --from=builder /dist/ /tmp/dist/
COPY docker-entrypoint.sh /usr/local/bin/kicad-mcp-pro-entrypoint
RUN python -m pip install --no-cache-dir \
    --requirement /tmp/dist/requirements.txt \
    /tmp/dist/*.whl \
  && rm -rf /tmp/dist \
  && chmod 0755 /usr/local/bin/kicad-mcp-pro-entrypoint

USER kicadmcp
ENTRYPOINT ["kicad-mcp-pro-entrypoint"]
