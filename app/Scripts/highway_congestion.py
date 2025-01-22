# library imports block
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable  # Import Variable to fetch Airflow variables

# Define file paths as variables 
TARGET_DIR = Variable.get("target", "/default/output/path")
STAGING_DIR = Variable.get("staging", "/default/staging/path")

# defining dag arguments
default_args={
    'owner': 'Marilyn Croffie',
    'start_date': days_ago(0),
    'email': ['marilyn.croffie@mnsu.edu'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# dag definition
dag=DAG(
    dag_id='ETL_toll_data',
    schedule_interval=timedelta(days=1),
    default_args=default_args,
    description='highway congestion analysis: etl pipeline for toll data',
)

# Define the BashOperator tasks
download_data = BashOperator(
    task_id='download_data',
    bash_command=f"wget -P {destination_dir} https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz",
    dag=dag,
)

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command=f'tar -zxvf {TARGET_DIR}/tolldata.tgz -C {TARGET_DIR}',
    dag=dag,
)

extract_data_from_csv = BashOperator( 
    task_id='extract_data_from_csv',
    bash_command=f"cut -d ',' -f1-4 {TARGET_DIR}/vehicle-data.csv | sed 's/\\r//g' > {TARGET_DIR}/csv_data.csv",
    dag=dag,
)

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command=f"cut -f5-7 < {TARGET_DIR}/tollplaza-data.tsv | tr '\\t' ',' | sed 's/\\r//g' > {TARGET_DIR}/tsv_data.csv",
    dag=dag,
)

extract_data_from_fixed_width_file = BashOperator(
    task_id='extract_data_from_fixed_width_file',
    bash_command=f"awk '{{print $(NF-1),$NF}}' {TARGET_DIR}/payment-data.txt | tr ' ' ',' | sed 's/\\r//g' > {TARGET_DIR}/fixed_width_data.csv",
    dag=dag,
)

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command=f'paste -d "," {TARGET_DIR}/csv_data.csv {TARGET_DIR}/tsv_data.csv {TARGET_DIR}/fixed_width_data.csv > {TARGET_DIR}/extracted_data.csv',
    dag=dag,
)

transform_load_data = BashOperator(
    task_id='transform_load_data',
    bash_command=f"awk -F',' -v OFS=',' '{{ $4=toupper($4) }} 1' {TARGET_DIR}/extracted_data.csv > {STAGING_DIR}/transformed_data.csv",
    dag=dag,
)

# Task pipeline
download_data >> unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width_file >> consolidate_data >> transform_load_data
