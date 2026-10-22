CREATE TABLE IF NOT EXISTS test_runs (
    run_id       SERIAL PRIMARY KEY,
    started_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    environment  VARCHAR(50) NOT NULL DEFAULT 'local'
);

CREATE TABLE IF NOT EXISTS test_results (
    result_id         SERIAL PRIMARY KEY,
    run_id            INT NOT NULL REFERENCES test_runs(run_id),
    suite             VARCHAR(50) NOT NULL,
    test_name         VARCHAR(255) NOT NULL,
    status            VARCHAR(10) NOT NULL,
    duration_seconds  NUMERIC(8,3),
    executed_at       TIMESTAMP NOT NULL DEFAULT NOW()
);