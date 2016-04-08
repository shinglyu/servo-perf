function printTime(name, t){
  var output = "[PERF]," + name + "," + t;
  console.log(output);
  //document.getElementById('timing').innerHTML += output + "<br/>";
}
window.addEventListener('load', function(){
  printTime("navigationStart", performance.timing.navigationStart);
  printTime("unloadEventStart", performance.timing.unloadEventStart);
  printTime("unloadEventEnd", performance.timing.unloadEventEnd);
  printTime("redirectStart", performance.timing.redirectStart);
  printTime("redirectEnd", performance.timing.redirectEnd);
  printTime("fetchStart", performance.timing.fetchStart);
  printTime("domainLookupStart", performance.timing.domainLookupStart);
  printTime("domainLookupEnd", performance.timing.domainLookupEnd);
  printTime("connectStart", performance.timing.connectStart);
  printTime("connectEnd", performance.timing.connectEnd);
  printTime("secureConnectionStart", performance.timing.secureConnectionStart);
  printTime("requestStart", performance.timing.requestStart);
  printTime("responseStart", performance.timing.responseStart);
  printTime("responseEnd", performance.timing.responseEnd);
  printTime("domLoading", performance.timing.domLoading);
  printTime("domInteractive", performance.timing.domInteractive);
  printTime("domContentLoadedEventStart", performance.timing.domContentLoadedEventStart);
  printTime("domContentLoadedEventEnd", performance.timing.domContentLoadedEventEnd);
  printTime("domComplete", performance.timing.domComplete);
  printTime("loadEventStart", performance.timing.loadEventStart);
  printTime("loadEventEnd", performance.timing.loadEventEnd);
});
