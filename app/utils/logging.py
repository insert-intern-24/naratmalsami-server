import logging
from discord_webhook import DiscordWebhook
from app.config import settings

class DiscordLogHandler(logging.Handler):
    def __init__(self, webhook_url: str):
        super().__init__()
        self.webhook_url = webhook_url

    def emit(self, record):
        try:
            log_entry = self.format(record)
            webhook = DiscordWebhook(url=self.webhook_url, content=log_entry)
            webhook.execute()
        except Exception:
            self.handleError(record)

def setup_logging():

    # 기본 로그 설정 (INFO 레벨)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    root_logger = logging.getLogger()

    # 일반 로그 핸들러: INFO 이상, 모든 로그 송출
    if settings.discord_webhook_general:
        general_handler = DiscordLogHandler(settings.discord_webhook_general)
        general_handler.setLevel(logging.INFO)
        general_handler.setFormatter(formatter)
        root_logger.addHandler(general_handler)

        # "uvicorn.access" 로거에도 핸들러 추가
        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        uvicorn_access_logger.setLevel(logging.INFO)
        uvicorn_access_logger.addHandler(general_handler)
        uvicorn_access_logger.propagate = True

    # 경고 이상 로그 핸들러: WARNING 이상만 송출
    if settings.discord_webhook_alert:
        alert_handler = DiscordLogHandler(settings.discord_webhook_alert)
        alert_handler.setLevel(logging.WARNING)
        alert_handler.setFormatter(formatter)
        root_logger.addHandler(alert_handler)

        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        uvicorn_access_logger.addHandler(alert_handler)
