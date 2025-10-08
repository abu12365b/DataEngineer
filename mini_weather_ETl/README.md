# Mini Weather ETL Pipeline 🌤️

A lightweight ETL (Extract, Transform, Load) pipeline for weather data processing using Apache Airflow, Docker, and Python.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a mini ETL pipeline that:
- **Extracts** weather data from external APIs (OpenWeatherMap, WeatherAPI, etc.)
- **Transforms** raw weather data into structured formats
- **Loads** processed data into databases or data warehouses
- **Orchestrates** the entire pipeline using Apache Airflow
- **Containerizes** the application using Docker for easy deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Weather APIs  │────│  ETL Pipeline   │────│   Data Store    │
│                 │    │                 │    │                 │
│ • OpenWeather   │    │ • Extract       │    │ • PostgreSQL    │
│ • WeatherAPI    │    │ • Transform     │    │ • CSV Files     │
│ • Others        │    │ • Load          │    │ • Parquet       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                    ┌─────────────────┐
                    │   Apache        │
                    │   Airflow       │
                    │   (Orchestrator)│
                    └─────────────────┘
```

## ✨ Features

- 🔄 **Automated Data Pipeline**: Schedule and monitor weather data extraction
- 🐳 **Docker Support**: Containerized deployment for consistency across environments  
- 📊 **Data Transformation**: Clean, validate, and structure weather data
- 🎛️ **Airflow Integration**: Visual pipeline monitoring and management
- 📈 **Scalable Architecture**: Easy to extend with additional data sources
- 🔧 **Configurable**: Environment-based configuration management
- 📝 **Logging**: Comprehensive logging for debugging and monitoring

## 📋 Prerequisites

Before running this project, ensure you have:

- **Docker** (v20.10+)
- **Docker Compose** (v2.0+)
- **Python** (v3.8+) - if running locally
- **Git** for version control

### API Keys Required

- OpenWeatherMap API key (free tier available)
- WeatherAPI key (optional, for additional data sources)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/abu12365b/DataEngineer.git
cd mini_weather_ETl
```

### 2. Environment Setup

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp env .env
```

Edit the `.env` file with your configuration:

```env
# API Keys
OPENWEATHER_API_KEY=your_openweather_api_key_here
WEATHER_API_KEY=your_weather_api_key_here

# Database Configuration
DB_HOST=postgres
DB_PORT=5432
DB_NAME=weather_db
DB_USER=airflow
DB_PASSWORD=airflow

# Airflow Configuration
AIRFLOW_UID=1000
AIRFLOW_GID=0
```

### 3. Docker Setup

Build and start the containers:

```bash
# Build the Docker images
docker-compose build

# Start the services
docker-compose up -d
```

### 4. Initialize Airflow

```bash
# Initialize the Airflow database
docker-compose exec airflow-webserver airflow db init

# Create an admin user
docker-compose exec airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

## 💻 Usage

### Starting the Pipeline

1. **Access Airflow Web UI**: Navigate to `http://localhost:8080`
   - Username: `admin`
   - Password: `admin`

2. **Enable the DAG**: Find the `weather_etl_pipeline` DAG and toggle it on

3. **Trigger Manual Run**: Click the play button to trigger a manual run

### Monitoring

- **Airflow UI**: Monitor pipeline execution, logs, and task status
- **Logs**: Check container logs using `docker-compose logs -f [service_name]`

### Stopping the Pipeline

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (caution: this will delete data)
docker-compose down -v
```

## 📁 Project Structure

```
mini_weather_ETl/
├── dags/                     # Airflow DAG files
│   ├── weather_etl_dag.py   # Main ETL pipeline DAG
│   └── utils/               # Helper functions
├── ETL/                     # ETL processing scripts
│   ├── extract.py          # Data extraction logic
│   ├── transform.py        # Data transformation logic
│   ├── load.py            # Data loading logic
│   └── config.py          # Configuration management
├── Docker/                 # Docker configuration files
│   ├── Dockerfile         # Main application Dockerfile
│   └── airflow.dockerfile # Airflow-specific Dockerfile
├── data/                  # Data storage (created at runtime)
│   ├── raw/              # Raw extracted data
│   ├── processed/        # Transformed data
│   └── output/           # Final output data
├── logs/                 # Application logs (created at runtime)
├── docker-compose.yaml   # Docker Compose configuration
├── requirements.txt      # Python dependencies
├── env                   # Environment variables template
├── .env                 # Your environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Required |
| `WEATHER_API_KEY` | WeatherAPI key | Optional |
| `DB_HOST` | Database host | `postgres` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `weather_db` |
| `SCHEDULE_INTERVAL` | DAG schedule interval | `@daily` |

### Pipeline Configuration

Edit `ETL/config.py` to customize:
- Cities to fetch weather data for
- Data transformation rules
- Output formats and destinations
- API endpoints and parameters

## 📖 API Documentation

### Supported Weather APIs

1. **OpenWeatherMap**
   - Current weather data
   - 5-day forecast
   - Historical data (paid tiers)

2. **WeatherAPI**
   - Real-time weather
   - Forecast data
   - Historical weather

### Data Schema

The pipeline outputs standardized weather data with the following schema:

```json
{
  "timestamp": "2025-10-07T12:00:00Z",
  "city": "New York",
  "country": "US",
  "temperature": 22.5,
  "humidity": 65,
  "pressure": 1013.25,
  "weather_condition": "partly_cloudy",
  "wind_speed": 5.2,
  "wind_direction": 180
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Container fails to start**
   - Check Docker and Docker Compose versions
   - Ensure ports 8080 and 5432 are not in use
   - Verify `.env` file exists and has correct values

2. **API rate limits**
   - Check your API key limits
   - Adjust the schedule interval in the DAG
   - Implement caching strategies

3. **Database connection errors**
   - Ensure PostgreSQL container is healthy
   - Check database credentials in `.env`
   - Wait for database initialization to complete

### Logs and Debugging

```bash
# View all container logs
docker-compose logs

# View specific service logs
docker-compose logs airflow-webserver
docker-compose logs postgres

# Follow logs in real-time
docker-compose logs -f
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

For local development without Docker:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENWEATHER_API_KEY=your_key_here
```

## 📈 Future Enhancements

- [ ] Add more weather data providers
- [ ] Implement data quality checks
- [ ] Add real-time streaming capabilities
- [ ] Create dashboards with Grafana
- [ ] Add machine learning weather predictions
- [ ] Implement data archiving strategies

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you have any questions or run into issues:

1. Check the [troubleshooting section](#troubleshooting)
2. Search existing [GitHub Issues](https://github.com/abu12365b/DataEngineer/issues)
3. Create a new issue with detailed information

---

**Happy ETL-ing!** 🚀