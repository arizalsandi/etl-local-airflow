# ETL FROM LOCAL WITH AIRFLOW

ETL project from local into Data Warehouse using Airflow

## Data Source
1. CSV
2. JSON
3. SQLite
4. Excel file ( xls, xlsx )

## Prerequisite
1. Python 3.6.9 ( or more )
2. Apache Airflow 2.0.2
3. Pip3

## Set Up Some of Dependencies
I use Virtual Box Linux Ubuntu 18.04 inside Windows 10 for this project

1. Virtual Env

- Set Up Virtual Env to prevent any library versions problem
 
`pip3 install virtualenv`

 - Enter to your Virtual Env directory, then do this `virtualenv [your virtual env name folder]`
 
 - After you created your own, activate yours by `source env/bin/activate`

 2 Airflow
 - Enter to your Virtual Env, if you alrady have Python by globally you may need to install again some of library such as Python `sudo apt install python3.8` and Airflow `pip3 install apache-airflow` because these library are isolated with other global library

 - Export your airflow home by `export AIRFLOW_HOME=$(pwd)` to set default airflow home or you can put to your own path
 
 - Airflow need to initialize database by run this code `airflow db init` to save your airflow dependencies for example your login credential

 - Create user airflow by running this code :
 `
 airflow users create \
 --username [your username to login] \
 --firstname [your first name] \
 --lastname [your lastname] \
 --role Admin \
 --email [your email]`
 
 - After we finish with sort of step, open in different terminal to start your airflow webserver and scheduler
 `airflow webserver --port 8080`
 `airflow scheduler`
 
 - Check to your website and write in URL section `localhost:8080` to make sure your airflow running smoothly
 
 Here's some example after you success running your airflow :


 
 NOTE = Everytime you want to run your airflow webserver and scheduler, you need to activate your Virtual Env by run this ``source env/bin/activate`


    
