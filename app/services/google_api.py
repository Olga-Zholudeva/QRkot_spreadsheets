from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import COLUMN, DRIVE_VERSION, FORMAT, ROW, SHEETS_VERSION


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Метод для создания гугл-таблицы с отчетом на диске пользователя."""

    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", SHEETS_VERSION)
    spreadsheet_body = {
        "properties": {"title": f"Отчет на {now_date_time}", "locale": "ru_RU"},
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridProperties": {"rowCount": ROW, "columnCount": COLUMN},
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response["spreadsheetId"]
    return spreadsheetid


async def set_user_permissions(spreadsheetid: str, wrapper_services: Aiogoogle) -> None:
    """Метод для выдачи прав на доступ к таблице на диске."""

    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive", DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str, close_projects: list, wrapper_services: Aiogoogle
) -> None:
    """Метод для обновления данных в таблице на диске."""

    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", SHEETS_VERSION)
    table_values = [
        ["Отчет от", now_date_time],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]
    for res in close_projects:
        new_row = [res.name, str(res.close_date - res.create_date), res.description]
        table_values.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range="A1:E30",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
