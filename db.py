import psycopg2
import logging
import datetime
import os
import json


dir = os.path.dirname(os.path.abspath('db.py'))
try:
    from find_it.secret import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
except:
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_USER = os.environ.get('DB_USER')

from scraping.utils import *

today = datetime.date.today()
ten_days_ago = today - datetime.timedelta(10)

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB {}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, speciality_id FROM subscribers_subscribers WHERE is_active=%s;""", (True,))
    cities_qs = cur.fetchall()
    print(cities_qs)
    todo_list = {i[0]: set() for i in cities_qs}
    for i in cities_qs:
        todo_list[i[0]].add(i[1])
    print(todo_list)

    cur.execute(""" SELECT * FROM  scraping_site;""")
    sites_qs = cur.fetchall()
    sites = {i[0]: i[1] for i in sites_qs}

    print(sites)

    url_list = []
    for city in todo_list:
        for sp in todo_list[city]:
            tmp = {}
            cur.execute(""" SELECT site_id, url_address FROM scraping_url 
                            WHERE city_id=%s AND speciality_id=%s; """, (city, sp))
            qs = cur.fetchall()
            print(qs)
            if qs:
                tmp['city'] = city
                tmp['specialty'] = sp
                for item in qs:
                    site_id = item[0]
                    tmp[sites[site_id]] = item[1]
                url_list.append(tmp)

    print(url_list)
    all_data = []
    errors = []
    if url_list:
        for url in url_list:
            tmp = {}
            tmp_content = []
            
            j, e = djinni(url['djinni.co'])
            tmp_content.extend(j)
            errors.extend(e)

            # tmp_content.extend(rabota(url['Rabota.ua']))
            j, e = djinni(url['Rabota.ua'])
            tmp_content.extend(j)
            errors.extend(e)
            
            # tmp_content.extend(work(url['Work.ua']))
            j, e = djinni(url['Work.ua'])
            tmp_content.extend(j)
            errors.extend(e)
            
            # tmp_content.extend(dou(url['Dou.ua']))  
            j, e = djinni(url['Dou.ua'])
            tmp_content.extend(j)
            errors.extend(e)
            
            tmp['city'] = url['city']
            tmp['specialty'] = url['specialty']
            tmp['content'] = tmp_content
            all_data.append(tmp)

    print('get data')
    if all_data:
        for data in all_data:
            city = data['city']
            specialty = data['specialty']
            jobs = data['content']

            for job in jobs:
                cur.execute(
                    """ SELECT * FROM scraping_vacancy WHERE url=%s; """,
                    (job['href'],)
                )
                qs = cur.fetchone()
                if not qs:
                    cur.execute(""" INSERT INTO scraping_vacancy (city_id, speciality_id, title, 
                                url, description, company, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                                (city, specialty, job['title'], job['href'], job['descript'], job['company'], today))

    if errors:
        cur.execute(""" SELECT data FROM scraping_error WHERE timestamp=%s; """, (today,))
        err_qs = cur.fetchone()
        if err_qs:
            data = err_qs[0]
            data['errors'].extend(errors)
            cur.execute(""" UPDATE scraping_error SET data=%s WHERE timestamp=%s; """, (json.dumps(data), today,))
        else:
            data = {}
            data['errors'] = errors
            cur.execute("""INSERT INTO scraping_error (data, timestamp) 
                            VALUES (%s, %s); """, (json.dumps(data), today ))



    cur.execute(""" DELETE FROM  scraping_vacancy WHERE timestamp <=%s;""", (ten_days_ago,))

    conn.commit()
    cur.close()
    conn.close()