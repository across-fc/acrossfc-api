# stdlib
from typing import Dict
from datetime import date

# 3rd-party
from tabulate import tabulate

# Local
from ffxiv_clear_rates.database import Database
from ffxiv_clear_rates.model import TrackedEncounter, ClearRate, TRACKED_ENCOUNTERS
from .report import Report


def clear_rates(database: Database) -> Report:
    clear_rates: Dict[TrackedEncounter, ClearRate] = database.get_clear_rates(
        tracked_encounters=TRACKED_ENCOUNTERS)

    table = [
        [
            encounter.name,
            f"{clear_rates[encounter].clears} / {clear_rates[encounter].eligible_members}",
            f"{clear_rates[encounter].clear_rate * 100:.2f}%"
        ]
        for encounter in TRACKED_ENCOUNTERS
    ]

    data_str = tabulate(table,
                        headers=['Encounter', 'FC clears', 'FC clear rate'])

    return Report(
        ':white_check_mark:',
        f'Across Clear Rates: {date.today()}',
        None,
        data_str,
        None
    )
