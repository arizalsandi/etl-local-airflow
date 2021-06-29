import sqlite3
import pandas as pd
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

DATA_SOURCE = '/home/sandi/dataset/file_1000.xls'
DATABASE_LOCATION = '/home/sandi/output/db_file_1000.sqlite'
CSV_OUTPUT = '/home/sandi/output/file_1000.csv'

default_args = {
	'owner':'sandi',
	'email':'arizalsandi@gmail.com',
	'email_on_failure':True,
	}

dag = 	DAG(
	'ETL_Blank_Space_Week_1_File_1000',
	default_args = default_args,
	schedule_interval = None,
	start_date = days_ago(1),
	)

def extract_transform(**kwargs):
	ti = kwargs['ti']
	
	output_csv = CSV_OUTPUT
	df = pd.read_excel(DATA_SOURCE)
	df.drop(['Unnamed: 0','First Name.1'], axis = 1, inplace=True)
	df['Full Name'] = df['First Name'] + ' ' + df['Last Name']
	df['Gender'] = df['Gender'].apply(lambda x: 'M' if x == 'Male' else 'F')
	df = df.reindex(columns=['Id','First Name', 'Last Name','Full Name', 'Gender', 'Country', 'Age', 'Date'])
	df = df.to_csv(output_csv, index = False )
	ti.xcom_push('file_1000', output_csv)

def load(**kwargs):
	ti = kwargs['ti']
	input_csv = ti.xcom_pull(task_ids='extract_transform', key='file_1000')
	conn = sqlite3.connect(DATABASE_LOCATION)

	df = pd.read_csv(input_csv)
	df.to_sql('file_1000', conn, index=False, if_exists='replace')

	

start 		= DummyOperator(
			task_id='start',
			dag = dag)

end			= DummyOperator(
			task_id='end',
			dag = dag)

extract_transform_task	= PythonOperator(task_id='extract_transform',
			python_callable = extract_transform,
			dag = dag)

load_task	= PythonOperator(task_id='load',
			python_callable = load,
			dag = dag)

start >> extract_transform_task >> load_task >> end
	
	
