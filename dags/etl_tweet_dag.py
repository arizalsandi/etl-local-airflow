import sqlite3
import pandas as pd
import json
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

DATA_SOURCE = '/home/sandi/dataset/tweet_data.json'
DATABASE_LOCATION = '/home/sandi/output/db_tweet.sqlite'
CSV_OUTPUT = '/home/sandi/output/tweet.csv'


default_args = {
	'owner':'sandi',
	'email':'arizalsandi@gmail.com',
	'email_on_failure':True,
	}

dag = DAG(
	'ETL_Blank_Space_Week_1_tweet',
	default_args = default_args,
	schedule_interval = None,
	start_date = days_ago(1),
	)


def extract_transform(**kwargs):
	ti = kwargs['ti']
	
	output_csv = CSV_OUTPUT
	user_dict = []
	with open(DATA_SOURCE, "r") as value:
		for i in value:
			data_json = json.loads(i)
			user_value = {
				'id' : data_json['id'],
				'text' : data_json['text'],
				'language' : data_json['lang'],
				'username' : data_json['user']['screen_name'],
				'verified' : data_json['user']['verified'],
				'statuses_count' : data_json['user']['statuses_count'],
				'followers_count' : data_json['user']['followers_count'],
				'location' : data_json['user']['location'],
				'created_at' : data_json['user']['created_at'],
			}
			user_dict.append(user_value)
	
	df = pd.DataFrame(user_dict)
	df.to_csv(output_csv, index = False )
	ti.xcom_push('tweetdata', output_csv)

 
def load(**kwargs):
	ti = kwargs['ti']
	input_csv = ti.xcom_pull(task_ids='extract_transform', key='tweetdata')
	conn = sqlite3.connect(DATABASE_LOCATION)

	df = pd.read_csv(input_csv)
	df.to_sql('tweet', conn, index=False, if_exists='replace')

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