#!/usr/local/bin/python3

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import re

config_file = 'es-dev-creds.txt'

with open(config_file) as f:
  config = dict(x.rstrip().split('=') for x in f)
# compile the regexes and save the list
config['ignore-patterns'] = []
if config['ignore']:
    config['ignore'] = config['ignore'].split(',')
    for pattern in config['ignore']:
        config['ignore-patterns'].append(re.compile(pattern))

# import json
# print (json.dumps(config, indent=3))


awsauth = AWS4Auth(config['AWS_ACCESS_KEY_ID'], config['AWS_SECRET_ACCESS_KEY'], 'us-west-2', 'es')

if 'local' not  in config_file:
    es = Elasticsearch(
        hosts=[
                {
                    'host': config['host'],
                    'port': int(config['port'])
                }
            ],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
else:
    es = Elasticsearch(
        hosts=[
                {
                    'host': config['host'],
                    'port': int(config['port'])
                }
            ],
        connection_class=RequestsHttpConnection
    )

# We just want to delete all indices that don't have an alias pointing to them.
allIndexes = es.indices.get('*')
# this returns
# {
#     "tps_parsed_calc_123": {
#         "aliases": {
#             "tps_parsed_calc": {},
#         }
#         ...
#     }
# }

for index in allIndexes.keys():
    if not allIndexes[index]['aliases'] and '.' not in index: # keep stuff like '.kibana', '.monitoring...', ...
        print('index {} has no alias'.format(index))

        # if we match with any of the ignores, set the flag and do not delete
        isIgnored = False
        for pattern in config['ignore-patterns']:
            if pattern.match(index):
                isIgnored = True

        if isIgnored:
            print('ignoring...')
        else:
            print('deleting...')
            es.indices.delete(index=index)


# Run this in kibana dev for this
# GET _cat/indices?s=index&h=index
# allIndexes = [line.rstrip('\n') for line in open('es-bad-indices.txt')]

# GET _cat/aliases?s=index&h=index
# goodIndexes = [line.rstrip('\n') for line in open('es-good-indices.txt')]

# for index in allIndexes:
#     if ('.kibana' not in index) and (index not in goodIndexes):
        # print ("DELETE /{}".format(index))
