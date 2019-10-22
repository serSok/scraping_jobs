import psycopg2
import logging
import datetime
import requests

from find_it.secret import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, MAILGUN_KEY, API, ADMIN_EMAIL
from scraping.utils import *

today = datetime.date.today()
FROM_EMAIL = 'noreply@find_it_les2.heroku.com'
SUBJECT = 'Недостающие УРЛ {}'.format(today)


try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB {}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, speciality_id FROM subscribers_subscribers WHERE is_active=%s;""", (True,))
    qs = cur.fetchall()
    
    cur.execute(""" SELECT * FROM scraping_city; """)
    cities_qs = cur.fetchall()
    cities = {i[0]:i[1] for i in cities_qs}

    cur.execute(""" SELECT * FROM scraping_speciality; """)
    sp_qs = cur.fetchall()
    sp = {i[0]:i[1] for i in sp_qs}

    mis_urls = []
    cnt = 'отсутсвуют урлы на дату {} вот таких пар:'.format(today)
    for pair in qs:
        cur.execute(""" SELECT * FROM scraping_url 
                            WHERE city_id=%s AND speciality_id=%s; """, (pair[0], pair[1]))
        qs = cur.fetchall()
        if not qs:
            mis_urls.append((cities[pair[0]], sp[pair[1]]))
    if mis_urls:
        for p in mis_urls:
            cnt += "Город - {}, специальность - {}".format(p[0], p[1])
            requests.post(API, auth=("api", MAILGUN_KEY), 
                            data={"from": FROM_EMAIL, "to": ADMIN_EMAIL, "subject": SUBJECT, "text": cnt}
            )
    
    conn.commit()
    cur.close()
    conn.close()


