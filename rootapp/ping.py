import requests
from apscheduler.schedulers.background import BlockingScheduler

def ping():
    requests.get('http://127.0.0.1:5000/update')

scheduler = BlockingScheduler()
scheduler.add_job(ping, 'interval', seconds = 2)
scheduler.start()