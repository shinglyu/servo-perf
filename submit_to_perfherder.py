
import argparse
import json
import random
import string
from thclient import (TreeherderClient, TreeherderClientError,
                      TreeherderResultSetCollection, TreeherderJobCollection)
import time

def format_perf_data(perf_json):
    suites = []
    for testcase in perf_json:
        suite = {
            "name": testcase["testcase"],
            "value": testcase["domComplete"],
            "subtests":[]
        }
        for key, value in testcase.iteritems():
            if key == "testcase":
                continue
            if value is None:
                value = -1
            suite["subtests"].append({"name": key, "value": value})
        suites.append(suite)

    return (
        {
            "performance_data": {
                "framework": {"name": "talos"},
                "suites": suites
            }
        }
    )

# TODO: refactor this big function to smaller chunks
def submit(perf_data):
    # TODO: load the last commit json and populate the result set
    # TODO: what should the timestamp be?
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
        #trs.add_type( data['type'] )

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
        #print(trsc)


    # TODO: load the test result, re-format it and submit as perf artifact
    dataset = [
        {
            'project': 'servo',
            'revision': revision_id,
            'job': {
                'job_guid': job_guid,
                'product_name': 'servo',
                'reason': 'scheduler',
                # TODO:What is `who` for?
                'who': 'Servo',
                'desc': 'Servo Page Load Time Tests',
                'name': 'Servo Page Load Time',
                # The symbol representing the job displayed in
                # treeherder.allizom.org
                'job_symbol': 'PL',

                # The symbol representing the job group in
                # treeherder.allizom.org
                'group_symbol': 'SP',
                'group_name': 'Servo Perf',

                # TODO: get the real timing from the test runner
                'submit_timestamp': push_timestamp,
                'start_timestamp': push_timestamp,
                'end_timestamp': push_timestamp,

                'state': 'completed',
                'result': 'success',

                'machine': 'local-machine',
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
                'tier': 1,

                # the ``name`` of the log can be the default of "buildbot_text"
                # however, you can use a custom name.  See below.
                # TODO: point this to the log when we have them uploaded
                'log_references': [
                    {
                        'url': 'TBD',
                        'name': 'test log'
                        }
                    ],

                # The artifact can contain any kind of structured data associated with a test.
                'artifacts': [
                    {
                        'type': 'json',
                        'name': 'performance_data',
                        #'job_guid': job_guid,
                        'blob': perf_data
                        #{

                            #"performance_data": {
                            ##    # TODO: can we create a framwork on treeherder
                            #    # that is not `talos`?
                            #    "framework": {"name": "talos"},
                            #    "suites": [{
                            #        "name": "performance.timing.domComplete",
                            #        "value": random.choice(range(15,25)),
                            #        "subtests": [
                            #            {"name": "responseEnd", "value": random.choice(range(5,15))},
                            #            {"name": "loadEventEnd", "value": random.choice(range(25,29))}
                            #        ]
                            #    }]
                            #}
                        #}
                    },
                    {
                        'type': 'json',
                        'name': 'Job Info',
                        #'job_guid': job_guid,
                        "blob": {
                            "job_details": [
                                {
                                    "url": "https://www.github.com/servo/servo",
                                    "value": "website",
                                    "content_type": "link",
                                    "title": "Source code"
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
        tj.add_tier( data['job']['tier'] )
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

        #for log_reference in data['job']['log_references']:
        #    tj.add_log_reference( 'buildbot_text', log_reference['url'])

        # data['artifact'] is a list of artifacts
        for artifact_data in data['job']['artifacts']:
            tj.add_artifact(
                artifact_data['name'], artifact_data['type'], artifact_data['blob']
                )
        tjc.add(tj)

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
# Post the result collection to a project
#
# data structure validation is automatically performed here, if validation
# fails a TreeherderClientError is raised
    client.post_collection('servo', tjc)

def main():
    parser = argparse.ArgumentParser(description="Submit Servo performance data to Perfherder")
    parser.add_argument("json_file", help="the output json from runner")
    args = parser.parse_args()

    with open(args.json_file, 'rb') as f:
        result_json = json.load(f)

    perf_data = format_perf_data(result_json)

    submit(perf_data)
    print "Done!"


if __name__ == "__main__":
    main()
