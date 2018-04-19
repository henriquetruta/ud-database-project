#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import psycopg2

"""
1. What are the most popular three articles of all time? Which articles
have been accessed the most? Present this information as a sorted list
with the most popular article at the top.

Example:

"Princess Shellfish Marries Prince Handsome" — 1201 views
"Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
"Political Scandal Ends In Political Scandal" — 553 views

2. Who are the most popular article authors of all time? That is, when
you sum up all of the articles each author has written, which authors get
the most page views? Present this as a sorted list with the most popular
author at the top.

Example:

Ursula La Multa — 2304 views
Rudolf von Treppenwitz — 1985 views
Markoff Chaney — 1723 views
Anonymous Contributor — 1023 views
3. On which days did more than 1% of requests lead to errors? The log table
includes a column status that indicates the HTTP status code that the news
site sent to the user's browser. (Refer to this lesson for more information
about the idea of HTTP status codes.)

Example:

July 29, 2016 — 2.5% errors
"""

with psycopg2.connect("dbname=news") as db:

    cur = db.cursor()

    # First query. Most popular articles
    query1 = ("select a.title, count(*) as c "
              "from articles a, "
              "slugs_accessed l "
              "where a.slug = l.slug "
              "group by a.title "
              "order by c desc "
              "limit 3;")
    cur.execute(query1)
    print "Query 1. Most popular articles. Results:"
    for register in cur.fetchall():
        print '"%s": %s views' % (register[0], register[1])

    # Second query. Most popular authors
    query2 = ("select au.name, count(*) as c "
              "from articles a, "
              "authors au, "
              "slugs_accessed l "
              "where a.slug = l.slug "
              "and au.id = a.author "
              "group by au.name "
              "order by c desc "
              "limit 3;")
    cur.execute(query2)
    print "Query 2. Most popular authors. Results:"
    for register in cur.fetchall():
        print '%s: %s views' % (register[0], register[1])

    # Third query. The days with more than 1% error requests
    query3 = ("select day, trunc(percentage*100, 1) from "
              "  (select error.day, "
              "   error.c::DECIMAL / total.c as percentage from "
              "   total, error "
              "   where total.day = error.day "
              "   order by error.day) days "
              "where percentage > 0.01;")
    cur.execute(query3)
    print "Query 3. The days with more than 1% error requests. Results:"
    for register in cur.fetchall():
        print '%s: %s%% errors' % (register[0], register[1])

    cur.close()
