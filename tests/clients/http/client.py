from logging import Logger

import allure
from httpx import Client, Response, QueryParams, Headers

from tests.clients.http.logger_event_hook import HTTPLoggerEventHook
from tests.context.base import RequestContext, build_http_test_headers
from tests.tools.config.http import HTTPClientTestConfig


class HTTPTestClient:
    """
    Базовый HTTP API-клиент тестового слоя.
    Он не содержит знаний о конкретных сервисах
    и используется как фундамент для специализированных клиентов.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    @allure.step("Make GET request to {url}")
    def get(
            self,
            url: str,
            params: QueryParams | None = None,
            context: RequestContext | None = None
    ) -> Response:
        headers = Headers()

        if context:
            headers = Headers(build_http_test_headers(context))

        # HTTPTestClient не выполняет валидацию ответа
        # и не знает о доменных схемах.
        # Его задача - корректно выполнить HTTP-вызов
        # и вернуть "сырой" Response выше по стеку.
        return self.client.get(
            url=url,
            params=params,
            headers=headers
        )


def build_http_test_client(
        logger: Logger,
        config: HTTPClientTestConfig
) -> Client:
    """
    Фабрика создания httpx.Client.
    Все API-клиенты сервисов используют именно этот Client,
    что гарантирует единое поведение HTTP-взаимодействий.
    """

    # Инициализируем обработчик логирования HTTP-событий.
    # Он будет вызываться httpx автоматически: перед отправкой запроса и после получения ответа.
    logger_event_hook = HTTPLoggerEventHook(logger=logger)

    return Client(
        timeout=config.timeout,
        base_url=str(config.url),
        event_hooks={
            "request": [logger_event_hook.request],
            "response": [logger_event_hook.response],
        },
    )
