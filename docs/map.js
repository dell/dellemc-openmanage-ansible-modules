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