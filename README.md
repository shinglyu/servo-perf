Servo Page Load Time Test
==============

[Tracking Bug](https://github.com/servo/servo/issues/10452)

# Usage
* Clone the servo repo in the root dir of this repo
* Download [tp5n.zip](http://people.mozilla.org/~jmaher/taloszips/zips/tp5n.zip), extract it to `page_load_test/`
* Run `prepare_manifest.sh` to tranform the tp5n manifest to our format
* Compile release build
* Put your `servo` binary and `resources` folder in `servo/`
* Run `test_all.sh <path/to/test.manifest>`

# How it works
* The testcase is from tp5, every testcase will run 20 times, and we take the median.
* Each testcase is a subtest on Perfherder, and their summary time is the geometric mean of all the subtests.

# TODO
* Check which tp5 test runs forever
* Report to perfherder
