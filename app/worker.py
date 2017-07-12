import logging
import os
from datetime import timedelta

import api
from celery import Celery
from model import Player
from celery.utils.log import get_task_logger
from mongoengine import connect
from raven import Client
from raven.contrib.celery import register_signal, register_logger_signal

celery = Celery('CLASH_TASKS', broker=os.getenv('BROKER_URL'))
logger = get_task_logger(__name__)

client = Client(os.getenv('SENTRY_DSN'))
register_logger_signal(client)
register_logger_signal(client, loglevel=logging.INFO)
register_signal(client)
register_signal(client, ignore_expected=True)

connect(db='clashstats', host='db', connect=False)


@celery.task
def update_clans():
    logger.info("Updating all clans.")
    for tag in Player.objects.distinct('clan.tag'):
        logger.info(f"Updating player stats for {tag}.")
        clan = api.find_clan_by_tag(tag)
        responses = api.fetch_all_players(clan)
        [Player(**r.json()).save() for r in responses]


celery.conf.beat_schedule = {
    'update_clans': {
        'task': 'worker.update_clans',
        'schedule': timedelta(hours=8)
    }
}