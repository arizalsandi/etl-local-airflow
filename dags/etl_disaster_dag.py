import sqlite3
import pandas as pd
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

DATA_SOURCE = '/home/sandi/dataset/disaster_data.csv'
DATABASE_LOCATION = '/home/sandi/output/disaster_data.sqlite'
CSV_OUTPUT = '/home/sandi/output/disaster_data_transform.csv'

default_args = {
	'owner':'sandi',
	'email':'arizalsandi@gmail.com',
	'email_on_failure':True,
	}

dag = DAG(
	'ETL_Blank_Space_Week_1_Disaster',
	default_args = default_args,
	schedule_interval = None,
	start_date = days_ago(1),
	)

def extract_transform(**kwargs):
	ti = kwargs['ti']

	output_csv = CSV_OUTPUT
	df = pd.read_csv(DATA_SOURCE)
	df = df.dropna()
	df = df.drop_duplicates()
	df['text'] = df['text'].str.replace(r'[^a-zA-Z0-9]',' ',regex=True)
	df = df.to_csv(output_csv, index = False )
	ti.xcom_push('disaster', output_csv)

def load(**kwargs):
	ti = kwargs['ti']

	input_csv = ti.xcom_pull(task_ids='extract_transform', key='disaster')
	conn = sqlite3.connect(DATABASE_LOCATION)

	df = pd.read_csv(input_csv)
	df.to_sql('disaster', conn, index=False, if_exists='replace')

start 		= DummyOperator(
			task_id='start',
			dag = dag)

end			= DummyOperator(
			task_id='end',
			dag = dag)

extract_transform_task	= PythonOperator(task_id='extract_transform',
			python_callable = extract_transform,
			dag = dag)

load_task		= PythonOperator(task_id='load',
			python_callable = load,
			dag = dag)

start >> extract_transform_task >> load_task >> end
