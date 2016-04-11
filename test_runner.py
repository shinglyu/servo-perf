import runner

def test_log_parser():
    mock_log = '''
[PERF] perf block start
[PERF],testcase,http://localhost:8000/page_load_test/56.com/www.56.com/index.html
[PERF],navigationStart,1460358376
[PERF],unloadEventStart,undefined
[PERF],unloadEventEnd,undefined
[PERF],redirectStart,undefined
[PERF],redirectEnd,undefined
[PERF],fetchStart,undefined
[PERF],domainLookupStart,undefined
[PERF],domainLookupEnd,undefined
[PERF],connectStart,undefined
[PERF],connectEnd,undefined
[PERF],secureConnectionStart,undefined
[PERF],requestStart,undefined
[PERF],responseStart,undefined
[PERF],responseEnd,undefined
[PERF],domLoading,1460358376000
[PERF],domInteractive,1460358388000
[PERF],domContentLoadedEventStart,1460358388000
[PERF],domContentLoadedEventEnd,1460358388000
[PERF],domComplete,1460358389000
[PERF],loadEventStart,undefined
[PERF],loadEventEnd,undefined
[PERF] perf block end
Shutting down the Constellation after generating an output file or exit flag specified
'''

    expected = [{
        "testcase": "http://localhost:8000/page_load_test/56.com/www.56.com/index.html",
        "navigationStart": 1460358376,
        "unloadEventStart": None,
        "unloadEventEnd": None,
        "redirectStart": None,
        "redirectEnd": None,
        "fetchStart": None,
        "domainLookupStart": None,
        "domainLookupEnd": None,
        "connectStart": None,
        "connectEnd": None,
        "secureConnectionStart": None,
        "requestStart": None,
        "responseStart": None,
        "responseEnd": None,
        "domLoading": 1460358376000,
        "domInteractive": 1460358388000,
        "domContentLoadedEventStart": 1460358388000,
        "domContentLoadedEventEnd": 1460358388000,
        "domComplete": 1460358389000,
        "loadEventStart": None,
        "loadEventEnd": None
    }]
    result = runner.parse_log(mock_log)
    assert(expected == result)

def test_log_parser_complex():
    mock_log = '''
[PERF] perf block start
[PERF],testcase,http://localhost:8000/page_load_test/56.com/www.56.com/content.html
[PERF],navigationStart,1460358300
[PERF],unloadEventStart,undefined
[PERF],unloadEventEnd,undefined
[PERF],redirectStart,undefined
[PERF],redirectEnd,undefined
[PERF],fetchStart,undefined
[PERF],domainLookupStart,undefined
[PERF],domainLookupEnd,undefined
[PERF],connectStart,undefined
[PERF],connectEnd,undefined
[PERF],secureConnectionStart,undefined
[PERF],requestStart,undefined
[PERF],responseStart,undefined
[PERF],responseEnd,undefined
[PERF],domLoading,1460358376000
[PERF],domInteractive,1460358388000
[PERF],domContentLoadedEventStart,1460358388000
[PERF],domContentLoadedEventEnd,1460358388000
[PERF],domComplete,1460358389000
[PERF],loadEventStart,undefined
[PERF],loadEventEnd,undefined
[PERF] perf block end
Some other js error logs here

[PERF] perf block start
[PERF],testcase,http://localhost:8000/page_load_test/56.com/www.56.com/index.html
[PERF],navigationStart,1460358376
[PERF],unloadEventStart,undefined
[PERF],unloadEventEnd,undefined
[PERF],redirectStart,undefined
[PERF],redirectEnd,undefined
[PERF],fetchStart,undefined
[PERF],domainLookupStart,undefined
[PERF],domainLookupEnd,undefined
[PERF],connectStart,undefined
[PERF],connectEnd,undefined
[PERF],secureConnectionStart,undefined
[PERF],requestStart,undefined
[PERF],responseStart,undefined
[PERF],responseEnd,undefined
[PERF],domLoading,1460358376000
[PERF],domInteractive,1460358388000
[PERF],domContentLoadedEventStart,1460358388000
[PERF],domContentLoadedEventEnd,1460358388000
[PERF],domComplete,1460358389000
[PERF],loadEventStart,undefined
[PERF],loadEventEnd,undefined
[PERF] perf block end
Shutting down the Constellation after generating an output file or exit flag specified
'''
    expected = [{
        "testcase": "http://localhost:8000/page_load_test/56.com/www.56.com/content.html",
        "navigationStart": 1460358300,
        "unloadEventStart": None,
        "unloadEventEnd": None,
        "redirectStart": None,
        "redirectEnd": None,
        "fetchStart": None,
        "domainLookupStart": None,
        "domainLookupEnd": None,
        "connectStart": None,
        "connectEnd": None,
        "secureConnectionStart": None,
        "requestStart": None,
        "responseStart": None,
        "responseEnd": None,
        "domLoading": 1460358376000,
        "domInteractive": 1460358388000,
        "domContentLoadedEventStart": 1460358388000,
        "domContentLoadedEventEnd": 1460358388000,
        "domComplete": 1460358389000,
        "loadEventStart": None,
        "loadEventEnd": None
    },{
        "testcase": "http://localhost:8000/page_load_test/56.com/www.56.com/index.html",
        "navigationStart": 1460358376,
        "unloadEventStart": None,
        "unloadEventEnd": None,
        "redirectStart": None,
        "redirectEnd": None,
        "fetchStart": None,
        "domainLookupStart": None,
        "domainLookupEnd": None,
        "connectStart": None,
        "connectEnd": None,
        "secureConnectionStart": None,
        "requestStart": None,
        "responseStart": None,
        "responseEnd": None,
        "domLoading": 1460358376000,
        "domInteractive": 1460358388000,
        "domContentLoadedEventStart": 1460358388000,
        "domContentLoadedEventEnd": 1460358388000,
        "domComplete": 1460358389000,
        "loadEventStart": None,
        "loadEventEnd": None
    }]
    result = runner.parse_log(mock_log)
    assert(expected == result)
