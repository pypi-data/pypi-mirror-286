import json

from celery import shared_task

from afex_logger.log_service import AppLogService


@shared_task(name='submit_afex_log')
def submit_log_data(log_type, log_data: str):
    print("Here to process submit_log_data", log_type, log_data)
    try:
        data = json.loads(log_data)
        AppLogService().send_logs(log_type, data)
    except Exception as e:
        print(e)


@shared_task(name='submit_afex_log_test')
def submit_log_data_test():
    print("Here to process submit_log_data_test")
