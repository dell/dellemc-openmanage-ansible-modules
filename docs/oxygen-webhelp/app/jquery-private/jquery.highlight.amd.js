define(["jquery", "jquery.highlight"], function($, highlight) {
    /**
     * In this context: ($ === jQuery) = false;
     *
     * '$' is a local jQuery used in noConflict mode.
     * The non-AMD modules are not compatible with te 'noconflict' support of requireJS.
     * @see: http://requirejs.org/docs/jquery.html#noconflictmap
     */
    $.fn.highlight = jQuery.fn.highlight;
    $.fn.removeHighlight = jQuery.fn.removeHighlight;
    return highlight;
});