import os
import subprocess


def test_load(url):
    ua_script_path= "{}/user-agent-js".format(os.getcwd())
    test_cmd = "./servo/servo {url} --userscripts {ua} -o {png}".format(
        url=url,
        ua=ua_script_path,
        png="output.png"
    )

    log = subprocess.check_output(test_cmd, stderr=subprocess.STDOUT, shell=True)
    return log


def main():
    # Assume the server is up and running
    log = test_load('http://localhost:8000/page_load_test/56.com/www.56.com/index.html')
    print(log)

if __name__ == "__main__":
    main()
