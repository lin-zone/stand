import time
import multiprocessing

import schedule

from stand.crawler import crawl
from stand.validator import validate


def run_process(job_func, join=False):
    """使用多进程运行函数, join=True时阻塞进程"""
    job_process = multiprocessing.Process(target=job_func)
    job_process.start()
    if join:
        job_process.join()


def first_run():
    """第一次运行, 先获取IP, 然后再验证"""
    run_process(crawl, join=True)
    run_process(validate)


def schedule_run():
    """每20分钟获取一次IP, 每60分钟验证一次IP"""
    schedule.every(20).minutes.do(run_process, crawl)
    schedule.every(60).minutes.do(run_process, validate)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            break


def run(once=False):
    first_run()
    if not once:
        schedule_run()


if __name__ == "__main__":
    run()