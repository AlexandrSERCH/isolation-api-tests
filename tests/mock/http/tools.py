from typing import Annotated

from fastapi import Header, HTTPException, status

from tests.context.scenario import Scenario


def get_scenario_http(
        scenario: Annotated[Scenario | None, Header(alias="X-Test-Scenario")] = None
) -> Scenario:
    # Сценарий передаётся в каждом HTTP-запросе через заголовок.
    # Это сознательное архитектурное решение:
    # сценарий является явным входом системы, а не скрытым состоянием.

    if not scenario:
        # Отсутствие сценария — это не "пустой кейс",
        # а ошибка конфигурации теста или клиента.

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Test-Scenario header is required",
        )

    return scenario
