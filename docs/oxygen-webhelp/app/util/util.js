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
        }
    }
});
