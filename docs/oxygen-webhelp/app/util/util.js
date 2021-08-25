define(["parseuri"], function(parseUri){
    return {
        /**
         * @description Log messages and objects value into browser console
         */
        debug: function (message, object) {
            // Uncomment the lines below to enable debug.

            //object = object || "";
            //console.log(message, object);
        },

        /**
         * @description Returns all available parameters or empty object if no parameters in URL
         * @return {Object} Object containing {key: value} pairs where key is the parameter name and value is the value of parameter
         */
        getParameter : function (parameter) {
            this.debug("getParameter(" + parameter + ")");
            var whLocation = "";

            try {
                whLocation = window.location;
                var p = parseUri(whLocation);

                for (var param in p.queryKey) {
                    if (p.queryKey.hasOwnProperty(param) && parameter.toLowerCase() == param.toLowerCase()){
                        return p.queryKey[param];
                    }
                }
            } catch (e) {
                this.debug(e);
            }
        },

        isLocal : function () {
            this.debug("isLocal()");
            var whLocation = "";

            try {
                whLocation = window.location;
                var p = parseUri(whLocation);

                if (p.protocol == "http" || p.protocol == "https") {
                    return false;
                }
            } catch (e) {
                this.debug(e);
            }

            return true;
        },
		
		/**
		 * Function added by Dell 986204 for Client Dom XSS Scripting issues
		 * IDPL-15171
		 * Filter the original search query to avoid cross site scripting possibility.
		 *
		 * @param {string} searchInput The search query to process.
		 * @returns {string} The filtered search query.
		 */
		filterXSSExpression : function (searchInput){
			// Eliminate the cross site scripting possibility.
			searchInput = searchInput.replace(/</g, " ")
				.replace(/>/g, " ")
				.replace(/"/g, " ")
				.replace(/'/g, " ")
				.replace(/=/g, " ")
				.replace(/0\\/g, " ")
				.replace(/\\/g, " ")
				.replace(/\//g, " ")
				.replace(/  +/g, " ");

			/*  START - EXM-20414 */
			searchInput =
				searchInput.replace(/<\//g, "_st_").replace(/\$_/g, "_di_").replace(/%2C|%3B|%21|%3A|@|\/|\*/g, " ").replace(/(%20)+/g, " ").replace(/_st_/g, "</").replace(/_di_/g, "%24_");
			/*  END - EXM-20414 */

			searchInput = searchInput.replace(/  +/g, " ");
			searchInput = searchInput.replace(/ $/, "").replace(/^ /, " ");

			return searchInput;
		},
		
		
		/**
		 * Function added by Dell 986204 for Client Dom XSS Scripting issues
		 * IDPL-15171
		 * This function creates a new anchor element and uses location
		 * properties (inherent) to get the desired URL data. Some String
		 * operations are used (to normalize results across browsers).
		 **/
		parseURL : function (url) {
			var a =  document.createElement('a');
			a.href = url;
			return {
				source: url,
				protocol: a.protocol.replace(':',''),
				host: a.hostname,
				port: a.port,
				query: a.search,
				params: (function(){
					var ret = {},
						seg = a.search.replace(/^\?/, '').split('&'),
						len = seg.length, i = 0, s;
					for (;i<len;i++) {
						if (!seg[i]) { continue; }
						s = seg[i].split('=');
						ret[s[0]] = filterXSSExpression(s[1]);
					}
					return ret;
				})(),
				//file: (a.pathname.match(//([^/?#]+)$/i) || [,''])[1],
				file: (a.pathname.match(/\/([^\/?#]+)$/i) || [, ''])[1],
				hash: filterXSSExpression(a.hash.replace('#','')),
				path: a.pathname.replace(/^([^/])/,'/$1'),
				relative: (a.href.match(/tps?:\/\/[^\/]+(.+)/) || [, ''])[1],
				segments: a.pathname.replace(/^\//, '').split('/')
			};
		}
    }
});
