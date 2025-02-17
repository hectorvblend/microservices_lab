FROM python:3.9-slim

LABEL name=blend_example

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

SHELL ["/bin/bash", "-c"]

# Install poetry and compilation dependencies
RUN apt-get update && apt-get install -y
RUN pip install --upgrade pip
RUN groupadd dsuser
RUN useradd --create-home -g dsuser dsuser
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Install python dependencies in /.venv
COPY requirements.txt .

RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org cloudfront.net proxy.aetna.com" && \
    pip install uv && \
    uv venv && \
    uv pip compile requirements.txt --output-file requirements.in && \
    uv pip sync requirements.in

# Create and switch to a new user
WORKDIR /app

# Install application into container
COPY src/ ./src
USER dsuser

EXPOSE 8020
EXPOSE 5432
CMD python main.py