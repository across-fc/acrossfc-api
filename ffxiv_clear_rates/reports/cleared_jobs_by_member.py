# stdlib
from io import StringIO
from typing import List, Dict
from collections import defaultdict

# 3rd-party
from tabulate import tabulate

# Local
from ffxiv_clear_rates.database import Database
from ffxiv_clear_rates.model import Member, Job, TrackedEncounter
from .report import Report


def cleared_jobs_by_member(database: Database, encounters: List[TrackedEncounter]) -> Report:
    cleared_jobs = database.get_cleared_jobs()

    buffer = StringIO()

    for i, encounter in enumerate(encounters):
        if i > 0:
            buffer.write('\n\n')

        # TODO: Present better. People with same number of job clears should be presented the same

        # Manually do a group-by. itertools.groupby seems to be oddly random...
        member_cleared_jobs: Dict[Member, List[Job]] = defaultdict(list)
        for member_cleared_job in cleared_jobs[encounter.name]:
            member_cleared_jobs[member_cleared_job[0]].append(member_cleared_job[1])

        member_cleared_jobs = sorted(member_cleared_jobs.items(), key=lambda i: (-len(i[1]), i[0].name))

        buffer.write(f'[{encounter.name}]')
        buffer.write('\n\n')
        table = []
        for i, item in enumerate(member_cleared_jobs):
            table.append([
                item[0].name,
                len(item[1]),
                ", ".join(job.tla for job in item[1])
            ])
        buffer.write(tabulate(table,
                              headers=['Member', 'Total', 'Jobs'],
                              tablefmt="simple"))

    return Report(
        ':white_check_mark:',
        'Cleared Jobs by Member:',
        'Names displayed in alphabetical order',
        buffer.getvalue(),
        None
    )