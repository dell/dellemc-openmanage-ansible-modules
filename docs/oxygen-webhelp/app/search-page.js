/**
 * Load the libraries for the Search page.
 */
define(["require", "config"], function() {
    require(['search'], function() {
        require([
            'nav-links-loader',
            'searchAutocomplete',
            'webhelp',
            'template-module-loader'
        ]);
    });
});