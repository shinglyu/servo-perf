from thclient import (TreeherderClient, TreeherderClientError,
                      TreeherderResultSetCollection, TreeherderJobCollection)

import time
import string
import random
push_timestamp = int(time.time())
hashlen = len('8888637cb9f78f19cb8463ff174e81756805d8cf')
revision_id = ''.join(random.choice(string.letters + string.digits) for i in xrange(hashlen))
job_guid = ''.join(random.choice(string.letters + string.digits) for i in xrange(hashlen))

trsc = TreeherderResultSetCollection()

dataset = [
    {
        # The top-most revision in the list of commits for a push.
        'revision': revision_id,
        'author': 'somebody@somewhere.com',
        'push_timestamp': push_timestamp,
        'type': 'push',
        # a list of revisions associated with the resultset. There
        # should be at least
        # one.
        'revisions': [
            {
                'comment': 'Bug 123457 - MY TEST BUG',
                'revision': revision_id,
                'repository': 'servo',
                'author': 'Some Person <sperson@someplace.com>'

            }
        ]
    }
]

for data in dataset:

    trs = trsc.get_resultset()

    trs.add_push_timestamp( data['push_timestamp'] )
    trs.add_revision( data['revision'] )
    trs.add_author( data['author'])
    trs.add_type( data['type'] )

    revisions = []
    for revision in data['revisions']:

        tr = trs.get_revision()

        tr.add_revision(revision['revision'])
        tr.add_author(revision['author'])
        tr.add_comment(revision['comment'])
        tr.add_repository(revision['repository'])

        revisions.append(tr)

    trs.add_revisions(revisions)

    trsc.add(trs)

# Send the collection to treeherder

# See the authentication section below for details on how to get a
# hawk id and secret
client = TreeherderClient(protocol='http', host='local.treeherder.mozilla.org',
                          client_id='slyu', secret='d959b6e0-81d4-414a-b28c-a766fc32e3b4')

# Post the result collection to a project
#
# data structure validation is automatically performed here, if validation
# fails a TreeherderClientError is raised
client.post_collection('servo', trsc)


dataset = [
    {
        'project': 'servo',
        'revision': revision_id,
        'job': {
            'job_guid': job_guid,
            'product_name': 'servo',
            'reason': 'scheduler',
            'who': 'spidermonkey_info__mozilla-inbound-warnaserr',
            'desc': 'Linux x86-64 mozilla-inbound spidermonkey_info-warnaserr build',
            'name': 'SpiderMonkey --enable-sm-fail-on-warnings Build',
            # The symbol representing the job displayed in
            # treeherder.allizom.org
            'job_symbol': 'L',

            # The symbol representing the job group in
            # treeherder.allizom.org
            'group_symbol': 'SP',
            'group_name': 'Servo Perf',

            'submit_timestamp': push_timestamp,
            'start_timestamp': push_timestamp + 10,
            'end_timestamp': push_timestamp + 20,

            'state': 'completed',
            'result': 'success',

            'machine': 'bld-linux64-ec2-104',
            'build_platform': {
                'platform':'linux64', 'os_name': 'linux', 'architecture': 'x86_64'
                },
            'machine_platform': {
                'platform': 'linux64', 'os_name': 'linux', 'architecture': 'x86_64'
                },

            'option_collection': {'opt': True},

            # jobs can belong to different tiers
            # setting the tier here will determine which tier the job
            # belongs to.  However, if a job is set as Tier of 1, but
            # belongs to the Tier 2 profile on the server, it will still
            # be saved as Tier 2.
            'tier': 2,

            # the ``name`` of the log can be the default of "buildbot_text"
            # however, you can use a custom name.  See below.
            'log_references': [
                {
                    'url': 'http://ftp.mozilla.org/pub/mozilla.org/spidermonkey/...',
                    'name': 'buildbot_text'
                    }
                ],

            # The artifact can contain any kind of structured data associated with a test.
            'artifacts': [
                {
                    'type': 'json',
                    'name': 'performance_data',
                    #'job_guid': job_guid,
                    'blob': {
                        "performance_data": {
                            "framework": {"name": "talos"},
                            "suites": [{
                                "name": "cheezburger metrics",
                                "value": random.choice(range(5,15)),
                                "subtests": [
                                    {"name": "test1", "value": 20.0},
                                    {"name": "test2", "value": 30.0}
                                ]
                            }]
                        }
                    }
                },
                {
                    'type': 'json',
                    'name': 'Job Info',
                    #'job_guid': job_guid,
                    "blob": {
                        "job_details": [
                            {
                                "url": "https://www.mozilla.org",
                                "value": "website",
                                "content_type": "link",
                                "title": "Mozilla home page"
                            },
                            {
                                "value": "bar",
                                "content_type": "text",
                                "title": "Foo"
                            },
                            {
                                "value": "This is <strong>cool</strong>",
                                "content_type": "raw_html",
                                "title": "Cool title"
                            }
                        ]
                    }
                }
            ],

            # List of job guids that were coalesced to this job
            'coalesced': []
        }
    }
]

tjc = TreeherderJobCollection()

for data in dataset:

    tj = tjc.get_job()

    tj.add_revision( data['revision'] )
    tj.add_project( data['project'] )
    tj.add_coalesced_guid( data['job']['coalesced'] )
    tj.add_job_guid( data['job']['job_guid'] )
    tj.add_job_name( data['job']['name'] )
    tj.add_job_symbol( data['job']['job_symbol'] )
    tj.add_group_name( data['job']['group_name'] )
    tj.add_group_symbol( data['job']['group_symbol'] )
    tj.add_description( data['job']['desc'] )
    tj.add_product_name( data['job']['product_name'] )
    tj.add_state( data['job']['state'] )
    tj.add_result( data['job']['result'] )
    tj.add_reason( data['job']['reason'] )
    tj.add_who( data['job']['who'] )
    tj.add_tier( 1 )
    tj.add_submit_timestamp( data['job']['submit_timestamp'] )
    tj.add_start_timestamp( data['job']['start_timestamp'] )
    tj.add_end_timestamp( data['job']['end_timestamp'] )
    tj.add_machine( data['job']['machine'] )

    tj.add_build_info(
        data['job']['build_platform']['os_name'], data['job']['build_platform']['platform'], data['job']['build_platform']['architecture']
        )

    tj.add_machine_info(
        data['job']['machine_platform']['os_name'], data['job']['machine_platform']['platform'], data['job']['machine_platform']['architecture']
        )

    tj.add_option_collection( data['job']['option_collection'] )

    for log_reference in data['job']['log_references']:
        tj.add_log_reference( 'buildbot_text', log_reference['url'])

    # data['artifact'] is a list of artifacts
    for artifact_data in data['job']['artifacts']:
        tj.add_artifact(
            artifact_data['name'], artifact_data['type'], artifact_data['blob']
            )
    tjc.add(tj)

client = TreeherderClient(protocol='http', host='local.treeherder.mozilla.org',
                          client_id='slyu', secret='d959b6e0-81d4-414a-b28c-a766fc32e3b4')

# Post the result collection to a project
#
# data structure validation is automatically performed here, if validation
# fails a TreeherderClientError is raised
client.post_collection('servo', tjc)


