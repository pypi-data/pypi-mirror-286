"""Injector configuration to bind the test classes to their implementations."""
from injector import Injector, singleton, Binder

from .interfaces.ianalytics import IAnalyticsAPI
from .interfaces.iusecases import IReportUseCase, IReportTemplate, IReportConverter
from .interfaces.ilogger import ILogger

from .usecases.pull_reports import PullReport
from .usecases.report_templates import ReportTemplates
from .usecases.converter import ReportConverter
from .infrastructure.google_analytics_api import GoogleAnalyticsAPI
from .infrastructure.logger import Logger


def configure(additional_configurations: list = None):
    """Configure the injector with optional additional configurations"""

    injector = Injector()

    def default_configuration(binder: Binder):
        binder.bind(IAnalyticsAPI, to=GoogleAnalyticsAPI, scope=singleton)
        binder.bind(IReportUseCase, to=PullReport, scope=singleton)
        binder.bind(ILogger, to=Logger, scope=singleton)
        binder.bind(IReportTemplate, to=ReportTemplates, scope=singleton)
        binder.bind(IReportConverter, to=ReportConverter, scope=singleton)
    
    injector.binder.install(default_configuration)
    if additional_configurations:
        for config in additional_configurations:
            injector.binder.install(config)
    
    return injector