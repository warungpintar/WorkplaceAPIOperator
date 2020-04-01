Examples
=============

Installation/Usage:
*******************
As the package has not been published on PyPi yet, it CANNOT be install using pip.

For now, you only need the source code module from workplace_operator to use it.

Example one of our DAG
**************************************************
.. code-block:: python

    """This example demonstrates on simply our DAG in Warung Pintar using BashOperator
    """

    import datetime as dt
	import airflow
	from airflow import models
	from airflow import DAG
	from airflow.operators.bash_operator import BashOperator
	from dependencies import workplace_operator

	def on_dag_failure(context):
	    print_task_instances(context)

	def print_task_instances(context):
	    failed_alert = workplace_operator.WorkplaceAPIPostOperator(
	        task_id = 'failed_task',
	        recipientId= models.Variable.get('workplace_id_grup'),
	        token= models.Variable.get('git_token'),
	        type_user='group'
	        )
	    return failed_alert.execute(context=context)

	def on_dag_success(context):
	    print_task_success(context)

	def print_task_success(context):
	    success_alert = workplace_operator.WorkplaceAPIPostOperator(
	        task_id = 'success_task',
	        recipientId= models.Variable.get('workplace_id_grup'),
	        token= models.Variable.get('git_token'),
	        type_user='group'
	        )
	    return success_alert.execute_success(context=context)

	default_dag_args = {
	    'owner' : 'fadhilla',
	    'start_date' : airflow.utils.dates.days_ago(1),
	    'email_on_failure': True,
	    'email_on_retry': False,
	    'provide_context': True,
	    'retries': 1,
	    'retry_delay': dt.timedelta(minutes=5),
	    'project_id': models.Variable.get('gcp_project_id', default_var='warung-support')
	}

	with DAG(
	      'etl-popin-clustering',
	      description='etl-popin-clustering',
	      schedule_interval='35 0 * * *',
	      on_success_callback=on_dag_success,
	      default_args=default_dag_args) as dag:

	  etl_popin_clustering_area = BashOperator(task_id='etl-popin-clustering-area',on_failure_callback=on_dag_failure,
	  bash_command='PYTHONPATH=/home/airflow/gcs/data/dag_script python /home/airflow/gcs/data/dag_script/Popin_Clustering_Area.py')

	  etl_popin_clustering_area
