/**
 * Load the Main Page (index.html) libraries.
 */
define(["require", "config"], function() {
    require([
        'nav-links-loader',
        'searchAutocomplete',
        'webhelp',
        'search-init',
        'context-help',
        'template-module-loader'
    ]);
});
