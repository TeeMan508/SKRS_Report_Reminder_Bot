def form_pretty_report(progress: str, plans: str, problems: str):
    text = (
        "*📈 Прогресс:*\n"
        "```\n"
        f"{progress}\n"
        "```\n\n"
        
        "*📝 Планы:*\n"
        "```\n"
        f"{plans}\n"
        "```\n\n"
        
        "*❓ Вопросы:*\n"
        "```\n"
        f"{problems}\n"
        "```"
    )
    return text