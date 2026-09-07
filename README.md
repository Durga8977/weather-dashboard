# Weather Dashboard

An interactive weather dashboard application that fetches real-time weather data from public APIs and provides comprehensive weather information, forecasts, and visualizations.

## Features

- **Real-time Weather Data**: Current temperature, humidity, wind speed, precipitation
- **Weather Forecasts**: 5-day and hourly forecasts
- **Multiple Locations**: Search and manage multiple cities
- **Weather Alerts**: Get notified of severe weather conditions
- **Interactive Maps**: Visualize weather patterns on maps
- **Historical Data**: View weather history and trends
- **Air Quality**: Monitor air quality indices
- **Responsive UI**: Works on desktop, tablet, and mobile
- **Dark Mode**: Comfortable viewing in any lighting

## Tech Stack

**Backend:**
- Python 3.9+
- Flask / FastAPI
- SQLAlchemy ORM
- PostgreSQL

**Frontend:**
- React / Vue.js
- Tailwind CSS
- Chart.js / Plotly
- Leaflet.js (Maps)

**APIs:**
- OpenWeatherMap API
- Weather API (WeatherAPI.com)
- OpenWeather Air Pollution API

## Project Structure

```
weather-dashboard/
├── backend/
│   ├── app.py                 # Flask app initialization
│   ├── config.py              # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── models/                # Database models
│   ├── services/              # Business logic
│   ├── routes/                # API endpoints
│   └── utils/                 # Helper functions
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   └── App.jsx
│   └── package.json
├── notebooks/                 # Jupyter notebooks
├── tests/                     # Test suites
├── docker-compose.yml         # Docker setup
└── README.md
```

## Quick Start

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## API Keys Required

1. **OpenWeatherMap API**: https://openweathermap.org/api
2. **WeatherAPI**: https://www.weatherapi.com/
3. **Mapbox (Optional)**: https://www.mapbox.com/

## Installation

### Option 1: Local Development

1. Clone the repository
2. Install dependencies (see Quick Start)
3. Set environment variables
4. Run migrations: `flask db upgrade`
5. Start backend and frontend servers

### Option 2: Docker

```bash
docker-compose up
```

## API Endpoints

### Weather Data
- `GET /api/weather/current/<city>` - Current weather
- `GET /api/weather/forecast/<city>` - 5-day forecast
- `GET /api/weather/hourly/<city>` - Hourly forecast
- `GET /api/weather/history/<city>` - Historical data

### Locations
- `GET /api/locations` - List saved locations
- `POST /api/locations` - Add new location
- `DELETE /api/locations/<id>` - Remove location

### Alerts
- `GET /api/alerts` - Get active alerts
- `POST /api/alerts` - Create alert
- `DELETE /api/alerts/<id>` - Delete alert

### Air Quality
- `GET /api/air-quality/<city>` - Air quality data
- `GET /api/air-quality/forecast/<city>` - AQ forecast

## Configuration

Create a `.env` file in the backend directory:

```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/weather_db
OPENWEATHERMAP_API_KEY=your_api_key
WEATHERAPI_KEY=your_api_key
SECRET_KEY=your_secret_key
```

## Database Models

- **User**: User accounts and preferences
- **Location**: Saved weather locations
- **CurrentWeather**: Real-time weather data
- **Forecast**: Weather forecasts
- **Alert**: Weather alerts
- **AirQuality**: Air quality data
- **WeatherHistory**: Historical weather records

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a pull request

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_weather_service.py

# Run with coverage
pytest --cov=.
```

## Deployment

### Heroku

```bash
heroku create weather-dashboard-app
git push heroku main
heroku run flask db upgrade
```

### AWS

See `deployment/aws-deployment.md`

### Docker

```bash
docker build -t weather-dashboard .
docker run -p 5000:5000 weather-dashboard
```

## Performance Optimization

- Redis caching for API responses
- Database query optimization
- Frontend code splitting
- Image optimization
- Lazy loading for charts

## Troubleshooting

### API Key Issues
- Verify API keys are correctly set in `.env`
- Check API key usage limits
- Ensure APIs are activated in your account

### Database Issues
- Check PostgreSQL is running
- Run migrations: `flask db upgrade`
- Check database connection string

### Frontend Issues
- Clear browser cache
- Restart development server
- Check console for errors

## License

MIT License - see LICENSE file

## Support

For issues and feature requests, please open a GitHub issue.

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Weather notifications (push)
- [ ] Advanced analytics
- [ ] Integration with smart home devices
- [ ] Multi-language support
- [ ] Offline mode
- [ ] Weather comparison tool
- [ ] Custom weather alerts

## Resources

- [OpenWeatherMap Documentation](https://openweathermap.org/api)
- [WeatherAPI Documentation](https://www.weatherapi.com/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
