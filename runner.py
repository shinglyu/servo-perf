import argparse
import datetime
import json
import os
import subprocess
import sys

# Configurations: should be extracted as commandline parameters
# manifest_path = "./page_load_test/tp5o_8000.manifest"  # Run prepare_manifest.sh
# manifest_path = "./page_load_test/temp.manifest"  # Run prepare_manifest.sh
# manifest_path = "./page_load_test/test.manifest"  # Run prepare_manifest.sh
# output_path = "./output/perf-{:%Y%m%d-%H%M%S}.json".format(datetime.datetime.now())



def load_manifest(filename):
    with open(filename, 'rb') as f:
        text = f.read()
    return parse_manifest(text)


def parse_manifest(text):
    return filter(lambda x: x != "", map(lambda x: x.strip(), text.splitlines()))


def test_load(url):
    ua_script_path = "{}/user-agent-js".format(os.getcwd())
    test_cmd = "./servo/servo '{url}' --userscripts {ua} -x -o {png}".format(
        url=url,
        ua=ua_script_path,
        png="output.png"
    )

    print("Running test:")
    print(test_cmd)
    try:
        log = subprocess.check_output(test_cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print("Unexpected Fail:")
        print(e)
        print("You man want to re-run the test manually:\n{}".format(test_cmd))
    return log


def parse_log(log):
    # Probably use regex here?
    blocks = []
    block = []
    copy = False
    for line in log.splitlines():
        if line.strip() == ("[PERF] perf block start"):
            copy = True
        elif line.strip() == ("[PERF] perf block end"):
            copy = False
            blocks.append(block)
            block = []
        elif copy:
            block.append(line)

    def parse_block(block):
        timing = {}
        for line in block:
            key = line.split(",")[1]
            value = line.split(",")[2]

            if key == "testcase":
                timing[key] = value
            else:
                timing[key] = None if (value == "undefined") else int(value)
        return timing

    timings = map(parse_block, blocks)
    return timings
    # for block in blocks:
    #     timing


def save_result_json(results, filename):
    with open(filename, 'wb') as f:
        json.dump(results, f, indent=2)
    print("Result saved to {}".format(filename))


def main():
    parser = argparse.ArgumentParser(
        description="Run page load test on servo"
    )
    parser.add_argument("tp5_manifest",
                        help="the test manifest in tp5 format")
    parser.add_argument("output_file",
                        help="filename for the output json")
    args = parser.parse_args()

    try:
        # Assume the server is up and running
        testcases = load_manifest(args.tp5_manifest)
        results = []
        for testcase in testcases:
            log = test_load(testcase)
            result = parse_log(log)
            #results.append(result)
            results += result
            print(log)
        save_result_json(results, args.output_file)

    except KeyboardInterrupt:
        print("Test stopped by user, saving partial result")
        save_result_json(results, args.output_file)


if __name__ == "__main__":
    main()
