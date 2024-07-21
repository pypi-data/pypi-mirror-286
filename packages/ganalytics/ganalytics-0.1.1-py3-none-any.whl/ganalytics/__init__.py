from .domains.analytics import (
    DateRange,
    MetricData,
    DimensionData,
    ReportRow,
    GoogleAnalyticsReport,
)

from .infrastructure.google_analytics_api import GoogleAnalyticsAPI
from .infrastructure.logger import Logger
from .interfaces.ianalytics import (
    IAnalyticsAPI,
)
from .interfaces.ilogger import ILogger
from .interfaces.iusecases import (
    IReportUseCase,
    IReportTemplate,
    IReportConverter,
)
from .usecases.converter import ReportConverter
from .usecases.pull_reports import PullReport
from .usecases.report_templates import ReportTemplates
from .utils.errors import (
    AppError,
    EnvironmentVariableError,
    GoogleAnalyticsAPIError,
    ReportNotFoundError,
    ReportParamsError,
)
from .utils.validators import (
    BaseValidator,
    BaseUseCase,
    BaseRepository,
    BaseAPI,
)
from .config import configure
from .client import ReportClient


__all__ = [
    "DateRange",
    "MetricData",
    "DimensionData",
    "ReportRow",
    "GoogleAnalyticsReport",
    "GoogleAnalyticsAPI",
    "Logger",
    "IAnalyticsAPI",
    "ILogger",
    "IReportUseCase",
    "IReportTemplate",
    "IReportConverter",
    "ReportConverter",
    "PullReport",
    "ReportTemplates",
    "AppError",
    "EnvironmentVariableError",
    "GoogleAnalyticsAPIError",
    "ReportNotFoundError",
    "ReportParamsError",
    "BaseValidator",
    "BaseUseCase",
    "BaseRepository",
    "BaseAPI",
    "configure",
    "ReportClient"
]


__version__ = "0.0.1"

