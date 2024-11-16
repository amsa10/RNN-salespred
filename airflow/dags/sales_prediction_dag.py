from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scraper.scraper import scrape_sales_data
from scraper.forecast import predict_sales
from scraper.save_to_db import save_to_db

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 16),
    'retries': 1,
}

with DAG(
    'sales_prediction_dag',
    default_args=default_args,
    description='Sales Prediction Pipeline: Scrape, Forecast, Save Data',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Step 1: Scrape sales data
    scrape_task = PythonOperator(
        task_id='scrape_sales_data_task',
        python_callable=scrape_sales_data,
        op_args=['http://example.com/sales']
    )

    # Step 2: Forecast future sales
    forecast_task = PythonOperator(
        task_id='forecast_sales_task',
        python_callable=predict_sales,
        op_args=['{{ task_instance.xcom_pull(task_ids="scrape_sales_data_task") }}']
    )

    # Step 3: Save predicted sales data to DB
    save_to_db_task = PythonOperator(
        task_id='save_to_db_task',
        python_callable=save_to_db,
        op_args=['{{ task_instance.xcom_pull(task_ids="forecast_sales_task") }}']
    )

    # Set the task dependencies
    scrape_task >> forecast_task >> save_to_db_task
