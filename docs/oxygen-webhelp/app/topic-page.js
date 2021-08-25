/**
 * Load the libraries for the DITA topics pages.
 */
define(["require", "config"], function() {
    require([
        'polyfill',
        'menu',
        'toc',
        'searchAutocomplete',
        'webhelp',
        'search-init',
        'expand',
        'image-map',
        'template-module-loader',
        'bootstrap'
    ]);
});