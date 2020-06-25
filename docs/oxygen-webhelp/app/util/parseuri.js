define(function() {
	// FROM: https://github.com/get/parseuri/blob/master/index.js

    /**
     * Parses an URI
     *
     * @author Steven Levithan <stevenlevithan.com> (MIT license)
     * @api private
     */

	// Added support for "file:" protocol
    var re = /^(?:(?![^:@]+:[^:@\/]*@)(http|https|ws|wss|file):\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?((?:[a-f0-9]{0,4}:){2,7}[a-f0-9]{0,4}|[^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/;

    var parts = [
        'source', 'protocol', 'authority', 'userInfo', 'user', 'password', 'host', 'port', 'relative', 'path', 'directory', 'file', 'query', 'anchor'
    ];

    /**
	 * the parseUri function.
     */
    return function(str) {
        str = str.toString();
        var src = str,
            b = str.indexOf('['),
            e = str.indexOf(']');

        if (b != -1 && e != -1) {
            str = str.substring(0, b) + str.substring(b, e).replace(/:/g, ';') + str.substring(e, str.length);
        }

        var m = re.exec(str || ''),
            uri = {},
            i = 14;

        while (i--) {
            uri[parts[i]] = m[i] || '';
        }

        if (b != -1 && e != -1) {
            uri.source = src;
            uri.host = uri.host.substring(1, uri.host.length - 1).replace(/;/g, ':');
            // Keep square brackets
            uri.authority = uri.authority.replace(/;/g, ':');
            uri.ipv6uri = true;
        }

        // Parse parameters
        var q = {
            name: "queryKey",
            parser: /(?:^|&)([^&=]*)=?([^&]*)/g
        };

        uri[q.name] = {};
        uri[parts[12]].replace(q.parser, function ($0, $1, $2) {
            if ($1) uri[q.name][$1] = $2;
        });

        return uri;
    };

});