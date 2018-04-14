#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import psycopg2

"""
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

Example:

"Princess Shellfish Marries Prince Handsome" — 1201 views
"Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
"Political Scandal Ends In Political Scandal" — 553 views

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

Example:

Ursula La Multa — 2304 views
Rudolf von Treppenwitz — 1985 views
Markoff Chaney — 1723 views
Anonymous Contributor — 1023 views
3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

Example:

July 29, 2016 — 2.5% errors
"""

with psycopg2.connect("dbname=news") as db:

    cur = db.cursor()

    query1 = ("select a.title, count(*) as c "
              "from articles a, "
              "(select split_part(path, '/', 3) as slug from log "
              " where log.path LIKE '/article/%') l "
              "where a.slug = l.slug "
              "group by a.title "
              "order by c desc "
              "limit 3;")
    cur.execute(query1)
    for register in cur.fetchall():
        print '"%s": %s views' % (register[0], register[1])
    cur.close()
    print db