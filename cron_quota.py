#!/usr/bin/env python

import datetime
from config import *

def increasePagecountMonthly():
    current_time = datetime.datetime.now()
    current_month = current_time.month
    current_year = current_time.year
    now_update = int(current_time.strftime("%s"))
    print "UN*X timestamp of now", now_update
    print "Normal timestamp of now %d/%d/%d - %d:%d:%d" % (current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second)

    first_of_this_month = int(datetime.datetime(current_year, current_month, 1, 0, 0, 0, 0).strftime("%s"))

    lastupdate = int( db_cursor.execute( 'SELECT value FROM config WHERE key == "lastupdate";' ).fetchone()[0] )
    lastupdate_dt = datetime.datetime.fromtimestamp(lastupdate)
    print "UN*X timestamp of last update", lastupdate
    print "Normal timestamp of last update %d/%d/%d - %d:%d:%d" % (lastupdate_dt.year,lastupdate_dt.month,lastupdate_dt.day,lastupdate_dt.hour,lastupdate_dt.minute,lastupdate_dt.second)

    # Calculate how many months have passed since last update
    passed_months = (current_year*12 + current_month) - (lastupdate_dt.year*12 + lastupdate_dt.month)
    print "Months passed since last update:", passed_months

    if (lastupdate < first_of_this_month):
        # Increase pagequota for everyone by 100 if pagequota won't exceed 600, else set it to 600
        db_cursor.execute( 'UPDATE config SET value = ? WHERE key == "lastupdate";', [now_update] )
        print "# # # Updating...",
	for i in range(passed_months):
	    print i+1,
            db_cursor.execute( 'UPDATE users SET pagequota = CASE WHEN pagequota + 100 > ? THEN ? ELSE pagequota + 100 END;', [default_page_quota,default_page_quota])

increasePagecountMonthly()
db_conn.commit()
