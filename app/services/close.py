from datetime import datetime


def close(model):
    """Закрываем проект/пожертвование и добавляем сумму закрытия."""

    if model.full_amount == model.invested_amount:
        model.fully_invested = True
        model.close_date = datetime.now()
