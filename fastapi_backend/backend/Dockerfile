FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR src
EXPOSE ${PORT}

# Copy code.
COPY main.py $WORKDIR
COPY . $WORKDIR/backend
COPY ../core $WORKDIR

# Copy integration tests. For run in the server.
COPY ../../tests/integration/backend $WORKDIR/tests/integration
COPY ../../tests/integration/__init__.py $WORKDIR/test/integration
COPY ../../tests/integration/conftest.py $WORKDIR/test/integration

# Copy unit tests. For run in the server.
COPY ../../tests/unit/backend $WORKDIR/tests/integration
COPY ../../tests/unit/__init__.py $WORKDIR/test/unit
COPY ../../tests/unit/conftest.py $WORKDIR/test/unit

# Copy anather helpfully things.
COPY logs $WORKDIR
COPY static $WORKDIR

VOLUME ["/src/backend", "/src/core", "logs"]

RUN pip install --upgrade pip
RUN pip install -r ../core/requirements.txt/

HEALTHCHECK
    --interval=30s \
    --timeout=10s \
    --start-period=30s \
    --retries=3 \
    CMD curl -f http://localhost:${PORT}/admin || exit 1

CMD alembic upgrade head && uvicorn main:main
