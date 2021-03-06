from celery import Celery 
import os
import redis
from classes.images import Image
from classes.pdps import PDP, pdpscraper
from helper import *

app = Celery()
app.config_from_object("celery_settings")

@app.task
def hello():
    print ('hello')

@app.task
def imgstatus_task(queryset):
    styles = []
    for style in queryset:
        obj = Image(style)
        styles.append(obj)

    for style in styles: 
        style.url = style.add_url()
        style.status = style.check_status()
    
    results = []
    for style in styles:
        content = style.print_full
        results.append(content)
    
    return results

@app.task
def pdpscrape_task(queryset, info):
    styles = []
    for style in queryset: 
        obj = PDP(style, info)
        styles.append(obj)

    return pdpscraper(styles, info)