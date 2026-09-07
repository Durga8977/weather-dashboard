import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_caching import Cache
from flask_apscheduler import APScheduler
from config import config

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
scheduler = APScheduler()

def create_app(config_name=None):
    """
    Application factory function.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Flask application instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    scheduler.init_app(app)
    
    # Register blueprints
    from routes.weather import weather_bp
    from routes.locations import locations_bp
    from routes.alerts import alerts_bp
    from routes.air_quality import air_quality_bp
    from routes.health import health_bp
    
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    app.register_blueprint(air_quality_bp, url_prefix='/api/air-quality')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Schedule background jobs
    if not scheduler.running:
        scheduler.start()
        from services.scheduler import schedule_jobs
        schedule_jobs(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
