<img src="docs\assets\BLEND BANNER.jpeg" width=100%>

# L&L: Microservices

## Overview

L&L Data Platform is a comprehensive microservices-based solution designed to streamline both structured data ingestion and AI-driven messaging. This platform is divided into two core services:

1. Data Ingestion Service – Facilitates efficient data migration from CSV files to a relational database.

2. AI Messaging Service – Enables secure interaction with DeepSeek for intelligent data processing and analysis.

## Features

### Data Ingestion Service

- Batch Data Ingestion: Supports bulk insertion of up to 1000 records per request.

- REST API for Data Processing: Enables secure and structured data ingestion via HTTP endpoints.

- Automated Database Management: Utilizes PostgreSQL with an integrated Adminer UI for easy access.

- Containerized Deployment: Fully dockerized for seamless deployment.

- Cloud Ready: Compatible with cloud providers with minimal configuration.

- Automated Testing: Includes unit and integration tests for validation.

### AI Messaging Service

- DeepSeek Integration: Facilitates interaction with AI for message processing.

- Real-time API Requests: Enables dynamic queries and AI-generated responses.

- Secure Messaging Pipeline: Ensures safe and encrypted communication.

- Scalable Architecture: Supports multiple AI-driven operations.

## Architecture

The platform follows a microservices-oriented architecture with modular design principles:

- Connectors: Handle database interactions and API requests to DeepSeek.

- Controllers: Manage API endpoints and request handling.

- Services: Implement business logic for data validation, transformation, and AI messaging.

- Utilities: Provide helper functions and shared utilities.

- Database: PostgreSQL is used for structured data storage, with Adminer for visualization.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Docker

- Docker Compose

- Python 3.8+

- UV (Optional) for faster package management

### Running the Application

Set Up Environment Variables:

Create a .env file in the root directory.

Define database and DeepSeek API credentials:

```bash
POSTGRES_DB=mydatabase
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
DEEPSEEK_API_KEY=myapikey
```

Install Dependencies:

```bash
uv venv
uv pip compile requirements.in --output-file requirements.txt
uv pip sync requirements.txt
```

Start Database and Services:

```bash
docker-compose up
```

This will launch PostgreSQL and Adminer. Access Adminer at http://localhost:8080.

Run the API Server for local development:

```bash
python run.py
```

## API Documentation

For a detailed list of available API endpoints, please refer to the Swagger documentation.

## Deployment

This platform can be deployed to any cloud provider. Recommended strategies:

- Kubernetes: Deploy as microservices with Helm charts.

- AWS ECS or Azure Container Apps: Managed container orchestration.

- Serverless Options: Use AWS Lambda for AI processing and API Gateway for requests.

## Testing

To run the automated tests:

```bash
python unit_tests_launcher.py
```

## Contributions

Contributions are welcome! Please open an issue or submit a pull request with improvements.
