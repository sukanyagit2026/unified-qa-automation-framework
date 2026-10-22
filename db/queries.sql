-- 1. Pass rate per suite for the latest run (retries not counted)
SELECT suite,
       COUNT(*) AS total,
       COUNT(*) FILTER (WHERE status = 'passed') AS passed,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'passed') / COUNT(*), 1) AS pass_pct
FROM test_results
WHERE run_id = (SELECT MAX(run_id) FROM test_runs)
  AND status <> 'rerun'
GROUP BY suite;

-- 2. Ten slowest tests, averaged across all runs
SELECT test_name,
       ROUND(AVG(duration_seconds), 2) AS avg_seconds,
       COUNT(*) AS executions
FROM test_results
WHERE status <> 'rerun'
GROUP BY test_name
ORDER BY avg_seconds DESC
LIMIT 10;

-- 3. Flaky tests: tests that needed a retry
SELECT test_name, COUNT(*) AS retries
FROM test_results
WHERE status = 'rerun'
GROUP BY test_name
ORDER BY retries DESC;