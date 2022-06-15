# Celery Configuration Options
broker_url = "amqp://guest:guest@localhost/"
task_serializer = "json"
accept_content=['json']
result_serializer='json'
timezone = "Asia/Tashkent"
enable_utc=True
task_track_started = True
task_time_limit = 30 * 60
result_backend = 'django-db'
cache_backend = 'django-cache'
beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
beat_schedule = {
    "scheduled_task": {
        "task": "apps.request.tasks.say_count",
        "schedule": 10.0,
    }
}
