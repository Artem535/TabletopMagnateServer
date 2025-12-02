"""
This module configures the BlackSheep application before it starts.
"""
from blacksheep import Application
from blacksheep.server.diagnostics import get_diagnostic_app
from rodi import Container

from app.auth import configure_authentication
from app.docs import configure_docs
from app.errors import configure_error_handlers
from app.services import configure_services
from app.settings import Settings


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(services=services)

    configure_error_handlers(app)
    configure_authentication(app, settings)
    configure_docs(app, settings)
    return app


def get_app():
    try:
        return configure_application(*configure_services())
    except Exception as exc:
        return get_diagnostic_app(exc)


app = get_app()
