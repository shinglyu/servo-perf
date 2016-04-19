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

# TODO
* Build a python test runner
* Run tp5
* Report to perfherder
