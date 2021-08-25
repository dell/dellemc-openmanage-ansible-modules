/**
 * Load the Main Page (index.html) libraries.
 */
define(["require", "config"], function() {
    require([
        'polyfill',
        'menu',
        'searchAutocomplete',
        'webhelp',
        'search-init',
        'context-help',
        'template-module-loader',
        'bootstrap'
    ]);
});
