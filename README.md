Servo Page Load Time Test
==============

[Tracking Bug](https://github.com/servo/servo/issues/10452)

# Usage
## Build Servo
* Clone the servo repo
* Compile release build
* Run `git_log_to_json.sh` in the servo repo, save it as `revision.json`

## Prepare the local Perfherder
* Add `192.168.33.10    local.treeherder.mozilla.org` to `/etc/hosts`
* `git clone https://github.com/mozilla/treeherder; cd treeherder`
* `vagrant up`
* `vagrant ssh`
  * `./bin/run_gunicorn`
* Outside of vm, open `http://local.treeherder.mozilla.org` and login to create an account
* `vagrant ssh`
  * `./manage.py create_credentials slyu slyu@mozilla.com "description"`, the email has to match your logged in user
  * Copy the clinet secrent to your `runner.py`


## Prepare the test runner
* Clone this repo
* Download [tp5n.zip](http://people.mozilla.org/~jmaher/taloszips/zips/tp5n.zip), extract it to `page_load_test/`
* Put your `servo` binary, `revision.json` and `resources` folder in `servo/`
* Run `prepare_manifest.sh` to tranform the tp5n manifest to our format
* `virtualenv venv; source venv/bin/activate; pip install treeherder-client`
* Run `test_all.sh`

# How it works
* The testcase is from tp5, every testcase will run 20 times, and we take the median.
* Each testcase is a subtest on Perfherder, and their summary time is the geometric mean of all the subtests.

# TODO
* Check which tp5 test runs forever
* Report to perfherder
