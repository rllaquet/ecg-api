FROM python:3.11 as builder

# Install requirements to /root/.local
COPY ./requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt

FROM builder as builder-test

# Install dev requirements to /root/.local
COPY requirements-test.txt /requirements-test.txt
RUN pip install --user -r /requirements-test.txt

FROM python:3.11 as base

# Copy python dependencies from builder
COPY --from=builder /root/.local /root/.local

WORKDIR /app
COPY ./src /app
COPY ./scripts/wait-for-it.sh /utils/wait-for-it.sh

FROM base as test

# Copy python dependencies from builder-test
COPY --from=builder-test /root/.local /root/.local

COPY ./tests /app/tests