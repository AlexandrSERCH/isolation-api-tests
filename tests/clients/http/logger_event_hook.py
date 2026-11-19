from logging import Logger

from httpx import Request, Response


class HTTPLoggerEventHook:
    """
    Инфраструктурный обработчик событий HTTP-клиента.
    Используется для логирования запросов и ответов
    на уровне транспортного слоя.
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    def request(self, request: Request):
        # Вызывается httpx перед отправкой HTTP-запроса.
        self.logger.info(
            f"{request.method} {request.url} - Waiting for response"
        )

    def response(self, response: Response):
        # Вызывается httpx после получения ответа.
        request = response.request
        self.logger.info(
            f"{request.method} {request.url} - Status {response.status_code}"
        )
