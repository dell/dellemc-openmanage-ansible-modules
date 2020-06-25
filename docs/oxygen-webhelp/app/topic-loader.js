if (EMCKickstart === undefined) {
                var EMCKickstart = {};
            }
        EMCKickstart.webhelpLocales = {"en-us": true};
/**
 To add a topic, just add a line like:
 "key" : "url",
 That's the key in quotes, a colon, the url in quotes, followed by a comma.
 You can add comments by prefixing the line with double slash (//).
 **/
EMCKickstart.webhelpMap = {
	// Main Help File
	"main": "index.html",

    // this is here so you don't have to worry about trailing commas
    "dummy": "/"
};

/**
* If an old URL is given, redirect to the corresponding topic from the WebHelp Responsive
*/
var actualLocation = window.location.href;
var newLocation;

if (actualLocation.match(/\/[\w]+\.htm(l)?([\w#\-]+)?\?topic=/gi) != null) {
	var linkSearchPosition = actualLocation.lastIndexOf("?");
	var linkTopicPosition = actualLocation.lastIndexOf("/");

	if (linkSearchPosition != -1) {
		var linkSearch = actualLocation.substr(linkSearchPosition, actualLocation.length);
		var resourceId = linkSearch.split('=')[1];
		if (resourceId != null) {

			$.each(EMCKickstart.webhelpMap, function (key, value) {
				if (key == resourceId) {
					window.location.replace(actualLocation.substr(0, linkTopicPosition) + "/" + value);
				}
			});

		}
	}
}
if (actualLocation.match(/\/[\w\-]+\.htm(l)?([\w#\-]+)?\?context=/gi) != null) {
	var linkSearchPosition = actualLocation.lastIndexOf("?");
	var linkTopicPosition = actualLocation.lastIndexOf("/");

	if (linkSearchPosition != -1) {
		var linkSearch = actualLocation.substr(linkSearchPosition, actualLocation.length);
		var contextId = linkSearch.split('=')[1];
		if (contextId != null) {

			$.each(EMCKickstart.webhelpMap, function (key, value) {
				if (key == contextId) {
					window.location.replace(actualLocation.substr(0, linkTopicPosition) + "/" + value);
				}
			});

		}
	}
}

if (actualLocation.indexOf('/#')!=-1) {
	newLocation = actualLocation.replace(/\/#/g, "/");
	window.location.replace(newLocation);
}
if (actualLocation.match(/\/index\.(.*)#/gi)!=null) {
	newLocation = actualLocation.replace(/\/index\.(.*)#/gi, "/");
	window.location.replace(newLocation);
}
			