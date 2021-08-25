define(function() {

    var modulePaths = {
        // core
        "webhelp" : "core/webhelp",
        "expand": "core/expand",
        "polyfill": "core/polyfill",
        // context sensitive help
        "context-help" : "context-help/context-help",
        "context-help-map" : "context-help/context-help-map",
        // navigation links
        "menu" : "nav-links/menu-loader",
        "toc" : "nav-links/toc-loader",
        "nav" : "nav-links/nav",
        // search
        "search-init" : "search/search-init",
        "search" : "search/search",
        "nwSearchFnt" : "search/nwSearchFnt",
        "searchAutocomplete" : "search/searchAutocomplete",
        "searchHistoryItems" : "search/searchHistoryItems",
        // search index
        "index" : "search/index/index",
        "link2parent" : "search/index/link-to-parent",
        "stopwords" : "search/index/stopwords",
        "index-1" : "search/index/index-1",
        "index-2" : "search/index/index-2",
        "index-3" : "search/index/index-3",
        "htmlFileInfoList" : "search/index/htmlFileInfoList",
        "keywords" : "search/index/keywords",
        // stemmers
        "stemmer" : "search/stemmers/stemmer",
        "en_stemmer" : "search/stemmers/en_stemmer",
        "de_stemmer" : "search/stemmers/de_stemmer",
        "fr_stemmer" : "search/stemmers/fr_stemmer",
        // options
        "options" : "options/options",
        "properties" : "options/properties",
        // utilities
        "util" : "util/util",
        "parseuri" : "util/parseuri",
        // i18n
        "localization" : "localization/localization",
        "strings" : "localization/strings",
        // image maps
        "image-map" : "image-map/image-map",

        // Publishing template JS module loader
        "template-module-loader" : "template/template-module-loader",
        // Publishing Template base directory
        "template-base-dir" : "../template",

        // jquery-private
        "jquery-private" : "jquery-private/jquery-private",
        "jquery.highlight.amd" : "jquery-private/jquery.highlight.amd",
        "jquery.bootpag.amd" : "jquery-private/jquery.bootpag.amd",
        "jquery.rwdImageMaps.amd" : "jquery-private/jquery.rwdImageMaps.amd",
        /********************************************************
         **************** 3rd Party Libraries *******************
         ********************************************************/

        // JQuery
        "jquery" : "../lib/jquery/jquery-3.5.1.min",
        // JQuery UI
        "jquery.ui" : "../lib/jquery-ui/jquery-ui.min",
        // JQuery Highlight
        "jquery.highlight" : "../lib/jquery-highlight/jquery.highlight-3",
        // JQuery Image maps highlighter
        "jquery.maphilight" : "../lib/maphighlight/jquery.maphilight.min",
        // JQuery Responsive image maps
        "jquery.rwdImageMaps" : "../lib/rwdImageMaps/jquery.rwdImageMaps.min",
        // JQuery Bootpag
        "jquery.bootpag" : "../lib/jquery-bootpag/jquery.bootpag.min",
        // Popper
        "bootstrap" : "../lib/bootstrap/js/bootstrap.bundle.min",

        "kuromoji" : "../lib/kuromoji/kuromoji"
    };

    var shimConfig = {
        // Responsive image maps
        "jquery.rwdImageMaps" : {
            deps: ["jquery"],
            exports : "jQuery.fn.rwdImageMaps"
        },
        // JQuery Highlight
        "jquery.highlight" : {
            deps: ["jquery"],
            exports : "jQuery.fn.highlight"
        },
        // JQuery Bootpag
        "jquery.bootpag" : {
            deps: ["jquery"],
            exports : "jQuery.fn.bootpag"
        },
    };

    requirejs.config({
        paths : modulePaths,
        shim : shimConfig,
        map: {
            // @see http://requirejs.org/docs/jquery.html#noconflictmap

            // '*' means all modules will get 'jquery-private'
            // for their 'jquery' dependency.
            "*": {
                     "jquery": "jquery-private",
                     "jquery.rwdImageMaps" : "jquery.rwdImageMaps.amd",
                     "jquery.highlight" : "jquery.highlight.amd",
                     "jquery.bootpag" : "jquery.bootpag.amd"
            },

            // 'jquery-private' wants the real jQuery module
            // though. If this line was not here, there would
            // be an unresolvable cyclic dependency.
            "jquery-private": { "jquery": "jquery" },
            "jquery.rwdImageMaps.amd" : {"jquery.rwdImageMaps" : "jquery.rwdImageMaps"},
            "jquery.highlight.amd" : {"jquery.highlight" : "jquery.highlight"},
            "jquery.bootpag.amd" : {"jquery.bootpag" : "jquery.bootpag"}

        }
    });
});