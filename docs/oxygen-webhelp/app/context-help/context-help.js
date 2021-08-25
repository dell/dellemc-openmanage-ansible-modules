define(["require", "util"], function (require, util) {
    $(document).ready(function () {
        // If we have a contextID, we must to redirect to the corresponding topic
        var contextId = util.getParameter('contextId');
        var appname = util.getParameter('appname');

        if (contextId != undefined && contextId != "") {
            require(["context-help-map"], function (helpContext) {
                if (helpContext != undefined) {
                    for (var i = 0; i < helpContext.length; i++) {
                        var ctxt = helpContext[i];
                        if (contextId == ctxt["appid"] && (appname == undefined || appname == ctxt["appname"])) {
                            var path = ctxt["path"];
                            if (path != undefined) {
                                
								/**
								 * Old code commented
								 * 
								 **/
								//var anchor = window.location.hash;
                                //window.location = path + anchor;-->
								
								/**
								 * This code has been added by Dell for IDPL-15171 Client Dom XSS Issue reported
								 * This code has reference to util.js file in the package to sanitize and encode  
								 * the url
								 * 
								 **/
								var srcurl = encodeURIComponent(window.location.href);
								var encodedurl = util.parseURL(srcurl);
								var parsedurl = util.parseURL(path + encodedurl.hash);
                                //var anchor = parsedurl.hash;
								window.location = encodeURIComponent(parsedurl);
                            }
                            break;
                        }
                    }
                }
            });
        }
    });
});