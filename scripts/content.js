console.log("Script injected")
//console.warn("Warned")


var filter = {urls: ["<all_urls>"]};

var callback = function(details) {
    alert("hello");
};

var opt_extraInfoSpec = [];

chrome.webRequest.onBeforeRequest.addListener(
        callback, filter, opt_extraInfoSpec);
