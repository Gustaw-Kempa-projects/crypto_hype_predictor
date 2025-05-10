from pathlib import Path
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import subprocess
import sqlite3

# ---------------------------------------------------------------------------
# 1. Resolve project folders inside the container
# ---------------------------------------------------------------------------
# dags/crypto_tracker_dag.py  →  parent().parent() == project root
BASE_DIR = Path(_file_).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
WAREHOUSE_DIR = BASE_DIR / "warehouse"
DB_PATH = WAREHOUSE_DIR / "raw_data.db"


# ---------------------------------------------------------------------------
# 2. Helper functions
# ---------------------------------------------------------------------------
def run_data_ingestion() -> None:
    """
    Executes scripts/data_ingestion.py with the same Python interpreter
    that is running this task (works inside Docker, CI, or locally).
    """
    script_path = SCRIPTS_DIR / "data_ingestion.py"
    subprocess.run(["python", str(script_path)], check=True)


def drop_tables() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(
            """
            DROP TABLE IF EXISTS main.names_data;
            DROP TABLE IF EXISTS main.ticker_data;
            DROP TABLE IF EXISTS main.data_raw_tickers;
            DROP TABLE IF EXISTS main.data_raw_names;
            """
        )
        conn.commit()


def delsert_final_data() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(
            """
            INSERT OR REPLACE INTO final_data (date, name, name_hype, ticker_hype, load_ts)
            SELECT
                n.date,
                n.instrument               AS name,
                n.value                    AS name_hype,
                t.value                    AS ticker_hype,
                strftime('%s', 'now')      AS load_ts
            FROM main.names_data  n
            LEFT JOIN main.names_dict   nd ON n.instrument = nd.name
            LEFT JOIN main.ticker_data  t  ON nd.ticker    = t.instrument;
            """
        )
        conn.commit()


# ---------------------------------------------------------------------------
# 3. DAG definition
# ---------------------------------------------------------------------------
default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="crypto_tracker_dag",
    default_args=default_args,
    schedule_interval=None,  # change to cron-string when you’re ready
    catchup=False,
    tags=["crypto"],
) as dag:

    clean_old_tables = PythonOperator(
        task_id="clean_old_tables",
        python_callable=drop_tables,
        pool="sqlite_write",  # 1-slot pool avoids locked-db errors
    )

    ingest_raw_data = PythonOperator(
        task_id="run_data_ingestion_script",
        python_callable=run_data_ingestion,
        pool="sqlite_write",  # writes too
    )

    run_unpivot_names = BashOperator(
        task_id="run_dbt_unpivot_names",
        bash_command="dbt run --select unpivot_names",
        cwd=str(BASE_DIR / "dbt"),  # working dir instead of cd …
    )

    run_unpivot_tickers = BashOperator(
        task_id="run_dbt_unpivot_tickers",
        bash_command="dbt run --select unpivot_tickers",
        cwd=str(BASE_DIR / "dbt"),
    )

    load_final_data = PythonOperator(
        task_id="load_final_data",
        python_callable=delsert_final_data,
        pool="sqlite_write",
    )

    (
        clean_old_tables
        >> ingest_raw_data
        >> run_unpivot_names
        >> run_unpivot_tickers
        >> load_final_data
    )
