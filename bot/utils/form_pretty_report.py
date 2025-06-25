from aiogram.utils.formatting import Code, as_list, Bold, Text


def form_pretty_report(user: str, progress: str, plans: str, problems: str) -> Text:
    return as_list(
        f"Отчет от @{user}",
        "",
        Bold("Прогресс:"),
        Code(progress),
        "",
        Bold("Планы:"),
        Code(plans),
        "",
        Bold("Вопросы:"),
        Code(problems),
    )