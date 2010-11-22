#!/usr/bin/env python
# encoding: utf-8

"""A quick-hack news scraper script for Boston; consumes RSS feeds.
"""

import datetime
import feedparser
import logging
import sys

from django.contrib.gis.geos import Point
from ebpub.db.models import NewsItem, Schema
from ebpub.geocoder.base import GeocodingException
from geocoder_hack import quick_dirty_fallback_geocode
from utils import log_exception

# Note there's an undocumented assumption in ebdata that we want to
# unescape html before putting it in the db.
from ebdata.retrieval.utils import convert_entities

logger = logging.getLogger()

def main(argv=None):
    logger.info("Starting add_news")
    if argv:
        url = argv[0]
    else:
        url = 'http://search.boston.com/search/api?q=*&sort=-articleprintpublicationdate&subject=massachusetts&scope=bonzai'
    schema_slug = 'local-news'

    try:
        schema = Schema.objects.get(slug=schema_slug)
    except Schema.DoesNotExist:
        logger.error( "Schema (%s): DoesNotExist" % schema_slug)
        sys.exit(1)

    f = feedparser.parse(url)
    addcount = updatecount = 0
    for entry in f.entries:
        title = convert_entities(entry.title)
        description = convert_entities(entry.description)

        if entry.id.startswith('http'):
            item_url = entry.id
        else:
            item_url = entry.link
        try:
            item = NewsItem.objects.get(schema__id=schema.id,
                                        title=title,
                                        description=description)
            #url=item_url)
            status = 'updated'
        except NewsItem.DoesNotExist:
            item = NewsItem()
            status = 'added'
        except NewsItem.MultipleObjectsReturned:
            # Seen some where we get the same story with multiple URLs. Why?
            logger.warn("Multiple entries matched title %r and description %r. Expected unique!" % (title, description))
            continue
        try:
            item.title = title
            item.schema = schema
            item.description = description
            item.url = item_url
            item.location_name = entry.get('x-calconnect-street') or entry.get('georss_featurename')
            item.item_date = datetime.datetime(*entry.updated_parsed[:6])
            item.pub_date = datetime.datetime(*entry.updated_parsed[:6])

            # feedparser bug: depending on which parser it magically uses,
            # we either get the xml namespace in the key name, or we don't.
            point = entry.get('georss_point') or entry.get('point')
            if point:
                x, y = point.split(' ')
            else:
                # Fall back on geocoding.
                text = item.title + ' ' + item.description
                try:
                    x, y = quick_dirty_fallback_geocode(text, parse=True)
                except GeocodingException:
                    logger.debug("Geocoding exception on %r:" % text)
                    log_exception(level=logging.DEBUG)
                    continue
                if None in (x, y):
                    logger.info("couldn't geocode '%s...'" % item.title[:30])
                    continue
            item.location = Point((float(y), float(x)))
            if item.location.x == 0.0 and item.location.y == 0.0:
                # There's a lot of these. Maybe attempt to
                # parse and geocode if we haven't already?
                logger.info("Skipping %r as it has bad location 0,0" % item.title)
                continue
            if not item.location_name:
                # Fall back to reverse-geocoding.
                from ebpub.geocoder import reverse
                try:
                    block, distance = reverse.reverse_geocode(item.location)
                    logger.debug(" Reverse-geocoded point to %r" % block.pretty_name)
                    item.location_name = block.pretty_name
                    item.block = block
                except reverse.ReverseGeocodeError:
                    logger.debug(" Failed to reverse geocode %s for %r" % (item.location.wkt, item.title))
                    item.location_name = u''
            item.save()
            if status == 'added':
                addcount += 1
            else:
                updatecount += 1
            logger.info("%s: %s" % (status, item.title))
        except:
            logger.error("Warning: couldn't save %r. Traceback:" % item.title)
            log_exception()
    logger.info("Finished add_news: %d added, %d updated" % (addcount, updatecount))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
