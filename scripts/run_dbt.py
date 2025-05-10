import subprocess
import os


def run_dbt_models():
    # Set the correct paths
    current_dir = os.getcwd()
    dbt_project_dir = os.path.join(
        current_dir, "crypto_tracker_project", "dbt"
    )  # Path to the dbt project directory
    profiles_dir = dbt_project_dir  # Path where profiles.yml is located

    # Print to verify the correct paths
    print(f"Running dbt models with profiles_dir: {profiles_dir}")
    print(f"Looking for dbt_project.yml in: {dbt_project_dir}")

    # Run dbt command for unpivot_names model
    try:
        print("Running dbt model: unpivot_names...")
        subprocess.run(
            [
                "dbt",
                "run",
                "--models",
                "unpivot_names",
                "--profiles-dir",
                profiles_dir,
                "--project-dir",  # Ensure dbt_project.yml is found
                dbt_project_dir,
            ],
            check=True,
        )
        print("Successfully ran dbt model: unpivot_names")
    except subprocess.CalledProcessError as e:
        print(f"Error running dbt model unpivot_names: {e}")

    # Run dbt command for unpivot_tickers model
    try:
        print("Running dbt model: unpivot_tickers...")
        subprocess.run(
            [
                "dbt",
                "run",
                "--models",
                "unpivot_tickers",
                "--profiles-dir",
                profiles_dir,
                "--project-dir",  # Ensure dbt_project.yml is found
                dbt_project_dir,
            ],
            check=True,
        )
        print("Successfully ran dbt model: unpivot_tickers")
    except subprocess.CalledProcessError as e:
        print(f"Error running dbt model unpivot_tickers: {e}")

    # Paths to the SQL files
    unpivot_names_path = os.path.join(dbt_project_dir, "unpivot_names.sql")
    unpivot_tickers_path = os.path.join(dbt_project_dir, "unpivot_tickers.sql")

    # Extract model names from file names
    model_names = [
        os.path.splitext(os.path.basename(unpivot_names_path))[0],
        os.path.splitext(os.path.basename(unpivot_tickers_path))[0],
    ]

    for model_name in model_names:
        print(f"Running dbt model: {model_name}...")
        result = subprocess.run(
            [
                "dbt",
                "run",
                "--select",
                model_name,
                "--profiles-dir",
                profiles_dir,
                "--project-dir",
                dbt_project_dir,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"Error running dbt model {model_name}:\n{result.stderr}")
        else:
            print(f"Successfully ran dbt model {model_name}!\n{result.stdout}")


if __name__ == "__main__":
    run_dbt_models()
