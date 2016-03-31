#!/usr/bin/env python

from azure.servicebus import ServiceBusService

import base64
import json
import optparse
import sys
import urllib2

mappings = {
  'topologies': 'topology/summary',
  'topology': 'topology/%(id)s'
}

def get_sbs(options):
  return ServiceBusService(options.host, shared_access_key_name=options.keyname, shared_access_key_value=options.key)

def main(argv):
  p = optparse.OptionParser(conflict_handler="resolve", description="This Zabbix plugin checks the health of an azure-servicebus instance.")

  p.add_option('-h', '--host', action='store', type='string', dest='host', default=None, help='The hostname you want to connect to')
  p.add_option('-k', '--key', action='store', type='string', dest='key', default=None, help='The access key to use for authentication')
  p.add_option('-n', '--keyname', action='store', type='string', dest='keyname', default='RootManageSharedAccessKey', help='The key name that the given access key relates to')

  p.add_option('-a', '--action', action='store', type='choice', dest='action', default=None, help='The action you want to take',
		                   choices=['topic-size', 'topic-percent', 'subscription-active'])
  p.add_option('-t', '--topic', action='store', type='string', dest='topic', default=None, help='The topic you want to interrogate')
  p.add_option('-s', '--subscription', action='store', type='string', dest='subscription', default=None, help='The subscription you want to interrogate')

  options, arguments = p.parse_args()

  if options.host is None or options.key is None or options.topic is None:
     return p.print_help()

  sbs = get_sbs(options)

  if options.action == 'topic-size':
    return get_topic_size(sbs, options.topic)
  elif options.action == 'topic-percent':
    return get_topic_percent(sbs, options.topic)
  elif options.action == 'subscription-active':
    return get_subscription_active(sbs, options.topic, options.subscription)
  else:
    p.print_help()

def get_topic_size(sbs, topic_name):
  print sbs.get_topic(topic_name).size_in_bytes

def get_topic_percent(sbs, topic_name):
  topic = sbs.get_topic(topic_name)
  max_size_in_bytes = topic.max_size_in_megabytes * 1024 * 1024
  size_in_bytes = topic.size_in_bytes
  print '%0.5f' % (float(size_in_bytes) / float(max_size_in_bytes))

def get_subscription_active(sbs, topic_name, subscription):
  subscr = sbs.get_subscription(topic_name, subscription)
  print subscr.message_count

#
# main app
#
if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
