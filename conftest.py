import os

import psycopg

DB_SETTINGS = {
    "host": os.getenv("QA_DB_HOST", "localhost"),
    "port": int(os.getenv("QA_DB_PORT", "5433")),
    "dbname": os.getenv("QA_DB_NAME", "qa_results"),
    "user": os.getenv("QA_DB_USER", "postgres"),
    "password": os.getenv("QA_DB_PASSWORD", "qa_pass"),
}

_conn = None
_run_id = None


def pytest_sessionstart(session):
    global _conn, _run_id
    try:
        _conn = psycopg.connect(**DB_SETTINGS, autocommit=True)
        with _conn.cursor() as cur:
            cur.execute(
                "INSERT INTO test_runs (environment) VALUES (%s) RETURNING run_id",
                (os.getenv("QA_ENV", "local"),),
            )
            _run_id = cur.fetchone()[0]
    except Exception as error:
        print(f"\n[results-db] Results will not be saved: {error}")
        _conn = None


def pytest_runtest_logreport(report):
    if _conn is None:
        return

    is_call = report.when == "call"
    is_setup_problem = report.when == "setup" and (report.failed or report.skipped)
    is_teardown_failure = report.when == "teardown" and report.failed
    is_rerun = report.outcome == "rerun"
    if not (is_call or is_setup_problem or is_teardown_failure or is_rerun):
        return

    suite = report.nodeid.split("/")[0]
    with _conn.cursor() as cur:
        cur.execute(
            "INSERT INTO test_results (run_id, suite, test_name, status, duration_seconds) "
            "VALUES (%s, %s, %s, %s, %s)",
            (_run_id, suite, report.nodeid[:255], report.outcome, round(report.duration, 3)),
        )


def pytest_sessionfinish(session, exitstatus):
    if _conn is not None:
        _conn.close()