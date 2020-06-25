/* Module that loads a user's custom module that was specified within the Publishing Template. */
define(["options", "util", "require"], function (options, util, require) {
    /**
     * @type {string}
     *
     * The ID of the Publishing Template base directory as it is specified in the configuration
     * object passed to the RequireJS library used to load the JS modules.
     */
    var TEMPLATE_BASE_DIR_ID = "template-base-dir";

    /**
     * @type {string}
     *
     * Specifies if the custom JavaScript module specified in the Publishing Template
     * should be loaded or not.
     */
    var isTemplateJsModuleLoadingEnabled = options.getBoolean('webhelp.enable.template.js.module.loading');

    /**
     * @type {string}
     *
     * The path of the template's main JS module relative to the base directory of the Publishing Template.
     */
    var templateMainJsModuleRelPath = options.get('webhelp.js.module.rel.path');

    if (isTemplateJsModuleLoadingEnabled && templateMainJsModuleRelPath) {
        var templateMainJsID = getTemplateMainJsID(templateMainJsModuleRelPath);
        try {
            require(
                [templateMainJsID],
                function() {
                   util.debug("Finished loading custom script:", templateMainJsModuleRelPath);
                },
                // Error callback
                function(err) {
                    console.error("Cannot load script:", templateMainJsModuleRelPath, err);
                }
            );
        } catch(err) {
            console.error("Cannot load script:", templateMainJsModuleRelPath, err);
        }
    }

    /**
     * Computes the ID of the template's main JS module.
     *
     * @param templateMainJsModuleRelPath The path of the template's main JS module
     *                              relative to the base directory of the Publishing Template.
     */
    function getTemplateMainJsID(templateMainJsModuleRelPath) {
        // Remove .js extension
        var ext = ".js";
        var templateMainJsRelPathNoExt;
        if (templateMainJsModuleRelPath.endsWith(ext)) {
            templateMainJsRelPathNoExt = templateMainJsModuleRelPath.substring(0, templateMainJsModuleRelPath.length - ext.length);
        } else {
            templateMainJsRelPathNoExt = templateMainJsModuleRelPath;
        }

        return TEMPLATE_BASE_DIR_ID + "/" + templateMainJsRelPathNoExt;
    }
});
