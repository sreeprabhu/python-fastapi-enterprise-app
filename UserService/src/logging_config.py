from logging.config import dictConfig

class TransactionIdFilter:
    def __call__(self, record):
        from UserService.src.middleware.transaction_context import get_transaction_id
        record.transaction_id = get_transaction_id() or "-"
        return True

def setup_logging():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "format": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "transaction_id": "%(transaction_id)s", "logger": "%(name)s", "message": "%(message)s", "pathname": "%(pathname)s", "lineno": %(lineno)d}',
            },
        },
        "filters": {
            "transaction_id_filter": {
                "()": TransactionIdFilter,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "filters": ["transaction_id_filter"],
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    })

# Filter fetches transaction ID from context variable
# JSON formatter includes transaction_id field
# Filter attached to logging configuration
# All console logs now include the transaction ID

#########################################################

# We choose to format our logs as JSON and log them to the console. 
# This is best practice if we later want to implement external services like Grafana for monitoring — which is highly relevant in an enterprise-grade setup, where you typically use a service like Grafana. 
# By logging in structured JSON, these tools can easily ingest, search, and visualise our logs, making it much easier to monitor service health, troubleshoot issues, and set up real-time alerts as our system scales.

