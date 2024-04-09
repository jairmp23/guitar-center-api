from .routes import health

def routes_config(app):
    app.include_router(health.router, prefix="/health")