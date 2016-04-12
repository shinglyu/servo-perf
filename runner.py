import os
import subprocess

# Configurations
manifest_path = "./page_load_test/tp5o_8000.manifest"  # Run prepare_manifest.sh


def test_load(url):
    ua_script_path = "{}/user-agent-js".format(os.getcwd())
    test_cmd = "./servo/servo '{url}' --userscripts {ua} -o {png}".format(
        url=url,
        ua=ua_script_path,
        png="output.png"
    )

    print("Running test:")
    print(test_cmd)
    log = subprocess.check_output(test_cmd, stderr=subprocess.STDOUT, shell=True)
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


def parse_manifest(text):
    return filter(lambda x: x != "", map(lambda x: x.strip(), text.splitlines()))


def load_manifest(filename):
    with open(filename, 'rb') as f:
        text = f.read()
    return parse_manifest(text)


def main():
    # Assume the server is up and running
    testcases = load_manifest(manifest_path)
    for testcase in testcases:
        log = test_load(testcase)
        result = parse_log(log)
        print(result)
    print(result)

if __name__ == "__main__":
    main()
