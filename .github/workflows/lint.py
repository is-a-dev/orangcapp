from __future__ import annotations

import requests
import os


def job1() -> bool:
    a = requests.request(
            "GET",
            f"https://api.github.com/repos/is-a-dev/orangcapp/pulls/{os.environ["PR_NUMBER"]}",
            headers={"Accept": "application/vnd.github+json"},
            timeout=60
        ).json()

    return a['user']['login'] == os.environ["LINT_CODE"]

result_1 = job1()

def job2() -> bool:
    a = requests.request(
            "GET",
            f"https://api.github.com/repos/is-a-dev/orangcapp/pulls/{os.environ["PR_NUMBER"]}/reviews",
            headers={"Accept": "application/vnd.github+json"},
            timeout=60
        ).json()
    
    l = [x for x in a if x['user']['login'] == os.environ["LINT_CODE"] and x['state'] == "APPROVED"]
    return len(l) > 0

result_2 = job2()


if not (result_1 or result_2): raise Exception

