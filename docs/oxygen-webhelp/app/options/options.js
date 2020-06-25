/* 
 * The 'properties.js' file is generated in the output directory next to this file
 *  and contains the parameters configured in the current transformation.
 */
define(['properties'], function (properties) {
    return {
        get : function (property) {
            return properties[property];
        },

        getBoolean : function (property) {
            var prop = properties[property];
            return prop == 'true' || prop == 'yes';
        },
        getIndexerLanguage : function() {
            // Implementation copied from IndexerTask.setIndexerLanguage()
            var language = this.get('webhelp.language');
            if (language) {
                var pos = language.indexOf('_');
                if (pos != -1) {
                    language = language.substring(0, pos);
                }
            }
            return language;
        }
    };
});