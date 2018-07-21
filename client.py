#!/usr/bin/env python

import json
import pymysql.cursors
import requests
import logging
import sys
import time

logging.basicConfig(level=logging.DEBUG)
args = sys.argv

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

with open('server.json') as json_data_file:
    extra_data = json.load(json_data_file)

logging.info('Config Loaded')

db = data['database']
server = extra_data['server']
key = data['key']
webservice_url = data['webservice_url']
headers = {'X-Api-Key' : key}
counter = 0

connection = pymysql.connect(host=db['host'],
                             user=db['user'],
                             password=db['password'],
                             db=db['name'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

logging.info('Database connection DONE')

sql = "select study_pk from study_service order by study_pk desc limit 1"

logging.info('Searching last Study PK in queue')

with connection.cursor() as cursor:
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is not None:
        if len(result) > 0:
            counter = int(result['study_pk'])

if len(args) > 1:
    if args[1] == 'initial':
        counter = -1

logging.info('Found: {} last study pk'.format(counter))

logging.info('Finding studies...')

sql = """
select patient.pk patient_pk,patient.pat_id patient_id,patient.pat_name patient_name,study.pk study_pk,study.study_iuid,study.study_datetime,study.study_desc study_description,study.mods_in_study study_modality,study.num_series study_series,study.num_instances study_instances from pacsdb.patient patient left join pacsdb.study study on study.patient_fk=patient.pk
"""

if counter >= 0:
    sql = '{} inner join study_service on study_service.study_pk=study.pk where study_service.study_pk<={}'.format(sql, counter)

#logging.info(sql)

with connection.cursor() as cursor:
    cursor.execute(sql)
    result = cursor.fetchall()

logging.info('Found studies and sending to WS')

cnt=0
for data in result:
    res = data
    res['center'] = server
    res['study_datetime'] = '{}'.format(res['study_datetime'])
    req = requests.post(webservice_url, json=res, headers=headers)
    cnt += 1
    if cnt >= 1000:
        time.sleep(2)
        cnt = 0
    logging.info(res['study_pk'])
    logging.info(req.text)


if counter > 0:
    sql = "delete from study_service where study_pk<={}".format(counter)
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()
    logging.info('Deleted studies in queue')