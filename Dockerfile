# Airflow 3.0.0, Python 3.12
FROM apache/airflow:3.0.0-python3.12

# Debian’s patched pip blocks root installs unless you allow it
ENV PIP_ROOT_USER_ACTION=ignore

# install ALL Python deps in a single layer
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

USER airflow