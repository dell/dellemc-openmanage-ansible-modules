define(['util', 'options', 'nwSearchFnt', 'searchHistoryItems', 'localization', 'jquery', 'jquery.highlight', 'jquery.bootpag'], function(util, options, nwSearchFnt, searchHistory, i18n, $) {

    /*
    	Oxygen WebHelp Plugin
    	Copyright (c) 1998-2020 Syncro Soft SRL, Romania.  All rights reserved.
    */

    var txt_browser_not_supported = "Your browser is not supported. Use of Mozilla Firefox is recommended.";

    /**
     * Constant with maximum search items presented for a single page.
     * @type {number}
     */
    var maxItemsPerPage = 10;

    /**
     * Variable with total page number.
     *
     * @type {number}
     */
    var totalPageNumber = -1;

    /**
     * Last displayed search results items.
     * @type {Array}
     */
    var lastSearchResultItems = [];

    /**
     * Last displayed search result.
     * @type {Array}
     */
    var lastSearchResult;

    /**
     * When it is true, then the score is displayed as tooltip.
     *
     * @type {boolean}
     */
    var displayScore = false;

    if(typeof String.prototype.trim !== 'function') {
        String.prototype.trim = function() {
            return $.trim(this);
        }
    }

    $(document).ready(function () {
        var searchQuery = '';
        try {
            searchQuery = util.getParameter('searchQuery');
            searchQuery = decodeURIComponent(searchQuery);
            
            // Eliminate the post and pre spaces int he input to avoid DOM XSS Issue 
            // JIRA - IDPL-16125 Code change added by 986204 on 12/8/2021
      	  searchQuery = searchQuery.trim();
            
            searchQuery = searchQuery.replace(/\+/g, " ");
            
            searchQuery = searchQuery.replace(/</g, " ")
            .replace(/>/g, " ")
            .replace(/"/g, " ")
            .replace(/'/g, " ")
            .replace(/=/g, " ")
            .replace(/0\\/g, " ")
            .replace(/\\/g, " ")
            .replace(/\//g, " ")
            .replace(/  +/g, " ");

             /*  START - EXM-20414 */
             searchQuery =
                 searchQuery.replace(/<\//g, "_st_").replace(/\$_/g, "_di_").replace(/%2C|%3B|%21|%3A|@|\/|\*/g, " ").replace(/(%20)+/g, " ").replace(/_st_/g, "</").replace(/_di_/g, "%24_");
             /*  END - EXM-20414 */
     
             searchQuery = searchQuery.replace(/  +/g, " ");
             searchQuery = searchQuery.replace(/ $/, "").replace(/^ /, " ");
            if (searchQuery.trim()!='' && searchQuery!==undefined && searchQuery!='undefined') {
                $('#textToSearch').val(searchQuery);
                util.debug("Execute search");
                executeQuery();
                util.debug("Executed search");
            }
        } catch (e) {
            util.debug("#########", e);
        }

        $('.gcse-searchresults-only').attr('data-queryParameterName', 'searchQuery');

        // Select page from parameter in the pages widget
        window.onpopstate = function(event) {
            if (lastSearchResultItems != null && lastSearchResult != null) {
                // Get the value for the 'page' parameter
                var pageToShow = util.getParameter("page");

                // Set to 1 if it is undefined
                if (pageToShow == undefined || pageToShow == "undefined" || pageToShow == "") {
                    pageToShow = 1;
                } else {
                    pageToShow = parseInt(pageToShow);
                    if (isNaN(pageToShow)) {
                        pageToShow = 1;
                    }
                }

                displayPageResults(pageToShow);

                // Update the active page
                $('.pagination li[class~="active"]').removeClass("active");
                $('.pagination li[data-lp="' + pageToShow + '"]:not([class~="prev"]):not([class~="next"])').addClass("active");

            }
        };

        $('#searchForm').on('submit', function(event){
            util.debug('submit form....');
            if ($('#textToSearch').val().trim()=='') {
                event.preventDefault();
                event.stopPropagation();

                return false;
            }
        });
    });


    /**
     * @description Search using Google Search if it is available, otherwise use our search engine to execute the query
     * @return {boolean} Always return false
     */
    function executeQuery() {
        util.debug("executeQuery");
        var input = document.getElementById('textToSearch');
        try {
            var element = google.search.cse.element.getElement('searchresults-only0');
        } catch (e) {
            util.debug(e);
        }
        if (element != undefined) {
            if (input.value == '') {
                element.clearAllResults();
            } else {
                element.execute(input.value);
            }
        } else {
            executeSearchQuery($("#textToSearch").val());
        }

        return false;
    }

    function clearHighlights() {

    }

    /**
     * Execute search query with internal search engine.
     *
     * @description This function find all matches using the search term
     * @param {HTMLObjectElement} ditaSearch_Form The search form from WebHelp page as HTML Object
     */
    function executeSearchQuery(query) {
        util.debug('SearchToc(..)');

        // Check browser compatibility
        if (navigator.userAgent.indexOf("Konquerer") > -1) {
            alert(i18n.getLocalization(txt_browser_not_supported));
            return;
        }

        searchAndDisplayResults(query);
    }

    function searchAndDisplayResults(query) {
        nwSearchFnt.performSearch(query, function(searchResult) {
            if (searchResult.searchExpression.trim().length > 0 || searchResult.excluded.length > 0) {
                displayResults(searchResult);
            } else {
                var error = searchResult.error;
                if (typeof error != "undefined" && error.length > 0) {
                    displayErrors(searchResult.error);
                }
            }
        });

    }

    /**
     * @description Display errors in HTML format
     * @param {string} errorMsg
     */
    function displayErrors(errorMsg) {
        var searchResultHTML = $('<p/>');
        searchResultHTML.addClass('errorMessage')
            .html(errorMsg);

        $('#searchResults').html(searchResultHTML);
    }

    /**
     * @description Display results in HTML format
     * @param {SearchResult} searchResult The search result.
     */
    function displayResults(searchResult) {

        preprocessSearchResult(searchResult, 'wh-responsive');

        // Add search query to history
        searchHistory.addSearchQueryToHistory(searchResult.originalSearchExpression);

        var webhelpEnableSearchPagination = options.getBoolean("webhelp.search.enable.pagination");
        var webhelpSearchNumberOfItems = options.getInteger("webhelp.search.page.numberOfItems");

        if (webhelpEnableSearchPagination !== 'undefined' && webhelpEnableSearchPagination == false) {
            // WH-1470 - Search pagination is disabled
            maxItemsPerPage = Number.MAX_VALUE;
        } else if (typeof webhelpSearchNumberOfItems !== 'undefined') {
            // WH-1471 - Option to control the maximum numbers of items displayed for each page
            maxItemsPerPage = webhelpSearchNumberOfItems;
        }

        // Compute the total page number
        totalPageNumber =
            Math.ceil(lastSearchResultItems.length / maxItemsPerPage);

        // Get the value for the 'page' parameter
        var pageToShow = util.getParameter("page");

        // Set to 1 if it is undefined
        if (pageToShow == undefined || pageToShow == "undefined" || pageToShow == "") {
            pageToShow = 1;
        } else {
            pageToShow = parseInt(pageToShow);
            if (isNaN(pageToShow)) {
                pageToShow = 1;
            }
        }

        // Display a page
        displayPageResults(pageToShow);

        if (totalPageNumber > 1) {
            // Add pagination widget
            $('#wh-search-pagination').bootpag({
                total: totalPageNumber,          // total pages
                page: pageToShow,            // default page
                maxVisible: 10,     // visible pagination
                leaps: false,         // next/prev leaps through maxVisible
                next: i18n.getLocalization("next.page"),
                prev: i18n.getLocalization("prev.page")
            }).on("page", function(event, num){
                util.debug("Display page with number: ", num);

                // Replace or add the page query
                var oldPage = util.getParameter("page");
                var oldQuery = window.location.search;
                var oldHref = window.location.href;
                var oldLocation = oldHref.substr(0, oldHref.indexOf(oldQuery));

                var newQuery = "";
                if (oldPage == undefined || oldPage == "undefined" || oldPage == "") {
                    newQuery = oldQuery + "&page=" + num;
                } else {
                    var re = new RegExp("(\\?|&)page\=" + oldPage);
                    newQuery = oldQuery.replace(re, "$1page="+num);
                }

                window.history.pushState("searchPage" + num, document.title, oldLocation + newQuery);

                displayPageResults(num);
                /*$("#content").html("Page " + num); // or some ajax content loading...
                 // ... after content load -> change total to 10
                 $(this).bootpag({total: 10, maxVisible: 10});*/
            });
        }
        // make bootpag compatible with Bootstrap 4.0
        $('#wh-search-pagination').find('li').addClass('page-item');
        $('#wh-search-pagination').find('a').addClass('page-link');

        $("#search").trigger('click');
    }

    /**
     * Display search results for a specific page.
     *
     * @param pageIdx The page index.
     */
    function displayPageResults(pageIdx) {
        var searchResultHTML =
            computeHTMLResult('wh-responsive', pageIdx, totalPageNumber, maxItemsPerPage);

        $('#searchResults').html(searchResultHTML);
        window.scrollTo(0, 0);
    }


    /***************************************************************************************
     ******************************* searchCommon.js****************************************
     **************************************************************************************/
    /**
     * An object containing the search result for a single topic/HTML page.
     * Contains pointer to the topicID, title, short description and the list of words that were found.
     *
     * @param {string} topicID The ID of the topic. Can be used to identify unique a document in the search result.
     * @param {string} relativePath The relative path to the topic.
     * @param {string} title The topic title.
     * @param {string} shortDescription The topic short description.
     * @param {[string]} words The array with words contained by this topic.
     * @param {int} scoring The search scoring computed for this document.
     * @param {int} startsWith The number used to display 5 stars ranking.
     * @param {int} resultID The search result ID.
     * @param {int} linkID The search link ID.
     * @param {[TopicInfo]} breadcrumb The breadcrumb of current document. Can be [].
     * @constructor
     */
    function SearchResultInfo(topicID, relativePath, title, shortDescription, words, scoring, starWidth, resultID, linkID, breadcrumb) {
        this.topicID = topicID;
        this.relativePath = relativePath;
        this.title = title;
        this.shortDescription = shortDescription;
        this.words = words;
        this.scoring = scoring;
        this.starWidth = starWidth;
        this.resultID = resultID;
        this.linkID = linkID;
        this.similarResults = [];
        this.breadcrumb = breadcrumb;
    }

    /**
     * Pre process search result to compute similar results and scoring.
     * The lastSearchResultItems variable will be updated.
     *
     * @param searchResult The seach result to process.
     * @param whDistribution The WebHelp distribution.
     */
    function preprocessSearchResult(searchResult, whDistribution) {
        lastSearchResult = searchResult;
        lastSearchResultItems = [];

        var wh_mobile =
            (typeof whDistribution != 'undefined') && whDistribution == 'wh-mobile';
        var wh_Classic =
            (typeof whDistribution != 'undefined') && whDistribution == 'wh-classic';


        if (searchResult.documents !== undefined && searchResult.documents.length > 0) {
            var allPages = searchResult.documents;
            
            // WH-1943 - sort by scoring, title and short description
            allPages.sort(function (first, second) {
                var cRes = second.scoring -first.scoring;
                if (cRes == 0) {
                    cRes = second.title.localeCompare(first.title);
                    if (cRes == 0) {
                        cRes = second.shortDescription.localeCompare(first.shortDescription);
                    }
                }
                return cRes;
            });
            // The score for fist item
            var ttScore_first = 1;
            if (allPages.length > 0) {
                ttScore_first = allPages[0].scoring;
            }

            var currentSimilarPage={};
            for (var page = 0; page < allPages.length; page++) {
                /*debug("Page number: " + page);*/

                if (allPages[page].relativePath == 'toc.html') {
                    continue;
                }

                var starWidth = 0;
                var webhelpSearchRanking = options.getBoolean("webhelp.search.ranking");
                if (typeof webhelpSearchRanking != "undefined" && webhelpSearchRanking) {
                    var hundredPercent = allPages[page].scoring + 100 * allPages[page].words.length;
                    var numberOfWords = allPages[page].words.length;
                    /*debug("hundredPercent: " + hundredPercent + "; ttScore_first: " + ttScore_first + "; numberOfWords: " + numberOfWords);*/
                    var ttScore = allPages[page].scoring;

                    // Fake value
                    var maxNumberOfWords = allPages[page].words.length;
                    starWidth = (ttScore * 100 / hundredPercent) / (ttScore_first / hundredPercent) * (numberOfWords / maxNumberOfWords);
                    starWidth = starWidth < 10 ? (starWidth + 5) : starWidth;
                    // Keep the 5 stars format
                    if (starWidth > 85) {
                        starWidth = 85;
                    }
                }

                var idLink = 'foundLink' + page;
                var idResult = 'foundResult' + page;

                // topicID, relativePath, title, shortDescription, words, scoring, starWidth, resultID, linkID, similarResults
                util.debug("page", page);
                var csri = new SearchResultInfo(
                    allPages[page].topicID,
                    allPages[page].relativePath,
                    allPages[page].title,
                    allPages[page].shortDescription,
                    allPages[page].words,
                    allPages[page].scoring,
                    starWidth,
                    idResult,
                    idLink,
                    allPages[page].breadcrumb
                );

                // Similar pages
                var similarPages = !wh_mobile && similarPage(allPages[page], allPages[page - 1]);
                if (!similarPages) {
                    currentSimilarPage = csri;
                    lastSearchResultItems.push(csri);
                } else {
                    currentSimilarPage.similarResults.push(csri);
                }

            }
        }
    }

    /**
     * Compute the HTML to be displayed in the search results page.
     *
     * @param whDistribution The string with WebHelp distribution. One of wh-classic, wh-mobile or wh-responsive.
     * @param pageNumber The page number to display.
     * @param totalPageNumber The total page number.
     * @param itemsPerPage The number of items to display on a page.
     * @returns {string} The HTML to be displayed as search result.
     */
    function computeHTMLResult(whDistribution, pageNumber, totalPageNumber, itemsPerPage) {
        // Empty jQuery element
        var results = $();

        var $wh_search_results_items = $();

        if (lastSearchResult.searchExpression.length > 0) {
            if (lastSearchResultItems.length > 0) {
                $wh_search_results_items = $('<div/>', {
                    class: 'wh_search_results_items'
                });

                // Start and end index depending on the current presented page
                var s = 0;
                var e = lastSearchResultItems.length;

                if (typeof pageNumber != "undefined" && typeof itemsPerPage != "undefined") {
                    s = (pageNumber - 1) * itemsPerPage;
                    var next = s + itemsPerPage;
                    e = Math.min(next, lastSearchResultItems.length);
                }

                // Result for: word1 word2
                var txt_results_for = "Results for:";
                var $headerHTML = $('<div/>', {
                    class: 'wh_search_results_header'
                });

                var $whSearchResultsHeaderDocs = $('<div/>', {
                    class: 'wh_search_results_header_docs'
                }).html(
                    lastSearchResultItems.length +
                    ' ' +
                    i18n.getLocalization(txt_results_for) + ' '
                );

                var $span = $('<span/>', {
                    class: 'wh_search_expression'
                }).html(lastSearchResult.originalSearchExpression);

                $whSearchResultsHeaderDocs.append($span);
                $headerHTML.append($whSearchResultsHeaderDocs);

                if (typeof pageNumber != "undefined" && typeof totalPageNumber != "undefined" && totalPageNumber > 1) {
                    var $wh_search_results_header_pages = $('<div/>', {
                        class: 'wh_search_results_header_pages'
                    }).html(i18n.getLocalization('Page') + ' ' + pageNumber + '/' + totalPageNumber);
                    $headerHTML.append($wh_search_results_header_pages);
                }

                $wh_search_results_items.append($headerHTML);

                // EXM-38967 Start numbering
                var start = (pageNumber - 1) * 10 + 1;
                var $ol = $('<ol/>', {
                    class: 'searchresult',
                    start: start
                });

                for (var page = s; page < e; page++) {
                    var csri = lastSearchResultItems[page];

                    var hasSimilarPages =
                        csri.similarResults != null &&
                        csri.similarResults.length > 0;

                    var siHTML = computeSearchItemHTML(
                        csri,
                        whDistribution,
                        hasSimilarPages,
                        null);
                    $ol.append(siHTML);

                    if (hasSimilarPages) {
                        // Add HTML for similar pages
                        for (var smPage = 0; smPage < csri.similarResults.length; smPage++) {
                            var simHTML = computeSearchItemHTML(
                                csri.similarResults[smPage],
                                whDistribution,
                                false,
                                csri.resultID);

                            $ol.append(simHTML);
                        }
                    }
                }

                $wh_search_results_items.append($ol);

                if ($wh_search_results_items.find('li').length == 0) {
                    $wh_search_results_items = $('<div/>', {
                        class: 'wh_search_results_for'
                    });
                    var $span = $('<span/>', {
                        class: 'wh_search_expression'
                    }).text(lastSearchResult.originalSearchExpression);

                    $wh_search_results_items.append($span);
                }
            } else {
                $wh_search_results_items = $('<div/>', {
                    class: 'wh_search_results_for'
                }).html(i18n.getLocalization('Search no results') + ' ');
                var $span = $('<span/>', {
                    class: 'wh_search_expression'
                }).text(lastSearchResult.originalSearchExpression);
                $wh_search_results_items.append($span);
            }
        } else {
            // Search expression is empty. If there are stop words, display a message accordingly
            if (lastSearchResult.excluded.length > 0) {
                $wh_search_results_items = $();
                var $p = $('<p/>', {
                    class: 'wh_search_results_for'
                }).html(i18n.getLocalization("no_results_only_stop_words1"));
                $wh_search_results_items.append($p);

                $p.html(i18n.getLocalization('no_results_only_stop_words2'));
                $wh_search_results_items.append($p);
            }
        }

        return $wh_search_results_items;
    }

    function computeSearchItemHTML(searchItem, whDistribution, hasSimilarPages, similarPageID) {
        // New empty jQuery element
        var htmlResult = $();

        var wh_mobile =
            (typeof whDistribution != 'undefined') && whDistribution == 'wh-mobile';
        var wh_Classic =
            (typeof whDistribution != 'undefined') && whDistribution == 'wh-classic';

        var allSearchWords = lastSearchResult.searchExpression.split(" ");

        var tempPath = searchItem.relativePath;

        // EXM-27709 START
        // Display words between '<' and '>' in title of search results.
        var tempTitle = searchItem.title;
        // EXM-27709 END
        var tempShortDesc = searchItem.shortDescription;
        var starWidth = searchItem.starWidth;
        var rankingHTML = $();

        var webhelpSearchRanking = options.getBoolean("webhelp.search.ranking");
        if (!wh_mobile && (typeof webhelpSearchRanking != 'undefined') && webhelpSearchRanking) {
            // Add rating values for scoring at the list of matches
            rankingHTML = $("<div/>", {
                id: 'rightDiv'
            });
            if (displayScore) {
                rankingHTML.attr('title', 'Score: ' + searchItem.scoring);
            }

            var rankingStar =
                $('<div/>', {
                    id: 'star'
                }).append(
                    $('<div/>', {
                        id: 'star0',
                        class: 'star'
                    }).append(
                        $('<div/>', {
                            id: 'starCur0',
                            class: 'curr',
                            style: 'width: ' + starWidth + 'px'
                        }).append(
                            $('<br/>', {
                                style: 'clear: both;'
                            })
                        )
                    )
                );
            rankingHTML.append(rankingStar);
        }

        var finalArray = searchItem.words;
        var arrayStringAux = [];
        var arrayString = '';
        var indexerLanguage = options.getIndexerLanguage().toLowerCase();
        var useCJKTokenizing = !!(typeof indexerLanguage != "undefined" && (indexerLanguage == "zh" ||
                                                                            indexerLanguage == "zh-cn" ||
                                                                            indexerLanguage == "zh-tw" ||
                                                                            indexerLanguage == "zh-hk" ||
                                                                            indexerLanguage == "ja" ||
                                                                            indexerLanguage == "ja-jp" ||
                                                                            indexerLanguage == "ko-kr" ||
                                                                            indexerLanguage == "ko"));

        for (var x in finalArray) {
            if (finalArray[x].length >= 2 || useCJKTokenizing) {
                arrayStringAux.push(finalArray[x]);
            }
        }
        arrayString = arrayStringAux.toString();

        // Add highlight param
        if (!wh_Classic && !wh_mobile) {
            tempPath += '?hl=' + encodeURIComponent(arrayString);
        }

        var idLink = searchItem.linkID;
        var idResult = searchItem.resultID;

        var link = 'return openAndHighlight(\'' + tempPath + '\', ' + arrayString + '\)';

        // Create the search result item li
        // Similar pages
        if (similarPageID == null) {
            htmlResult = $('<li/>', {
                id: idResult
            });
        } else {
            htmlResult = $('<li/>', {
                id: idResult,
                class: 'similarResult',
                'data-similarTo': similarPageID
            });
        }

        // The topic title of the search result item
        var $a = $('<a/>', {
            id: idLink,
            href: tempPath,
            class: 'foundResult'
        }).html(tempTitle);
        htmlResult.append($a);

        // The breadcrumb
        var breadcrumb = searchItem.breadcrumb;
        util.debug('searchItem', searchItem);
        util.debug('breadcrumb', breadcrumb);
        if (breadcrumb !== undefined && breadcrumb.length > 0) {
            // Show the breadcrumb
            var breadcrumbHtml = $('<div>', {
                class: 'search-breadcrumb',
            });

            var breadcrumbItems = $('<ol>');
            breadcrumb.forEach(function (item) {
                var li = $('<li>');
                var span = $('<span>',
                    {
                        class: 'title'
                    });
                span.append($('<a>',
                    {
                        href: item.relativePath,
                        html: item.title
                    }));
                li.append(span);
                breadcrumbItems.append(li);
            });

            breadcrumbHtml.append(breadcrumbItems);
            htmlResult.append(breadcrumbHtml);
        }

        // Short description
        // Also check if we have a valid description
        if ((tempShortDesc != "null" && tempShortDesc != '...')) {
            var $shortDescriptionDIV = $('<div/>', {
                class: 'shortdesclink'
            }).html(tempShortDesc);

            // Highlight the search words in short description
            for (var si = 0; si < allSearchWords.length; si++) {
                var sw = allSearchWords[si];
                $shortDescriptionDIV.highlight(sw, 'search-shortdescription-highlight');
            }

            htmlResult.append($shortDescriptionDIV);
        }

        // Empty jQuery element
        var searchItemInfo = $('<div/>', {
            class: 'missingAndSimilar'
        });

        // Relative Path
        $a = $('<a/>', {
            href: tempPath
        }).html(searchItem.relativePath);
        if (wh_Classic) {
            $a.attr('onclick', link);
        }

        var relPathStr = $('<div/>', {
            class: 'relativePath'
        }).append($a);

        searchItemInfo.append(relPathStr);

        // Missing words
        if (!useCJKTokenizing && !wh_mobile && allSearchWords.length != searchItem.words.length) {
            var missingWords = [];
            allSearchWords.forEach(function (word) {
                if (searchItem.words.indexOf(word) == -1) {
                    missingWords.push(word);
                }
            });

            var missingHTML = $('<div/>', {
                class: 'wh_missing_words'
            });
            missingHTML.html(i18n.getLocalization('missing') + ' : ');


            for (var widx = 0; widx < missingWords.length; widx++) {
                var $span = $('<span/>', {
                    class: 'wh_missing_word'
                }).text(missingWords[widx]);
                missingHTML.append($span).append(' ');
            }

            searchItemInfo.append(missingHTML);
        }

        if (!wh_mobile && hasSimilarPages) {
            var $similarHTML = $('<a/>', {
                class: 'showSimilarPages'
            }).html(i18n.getLocalization('Similar results') + '...');
            $similarHTML.click(showSimilarResults);
            searchItemInfo.append($similarHTML);
        }

        if (rankingHTML.html() != '' && searchItemInfo.html() != '') {
            var $searchItemAdditionalData = $('<div/>', {
                class: 'searchItemAdditionalData'
            }).append(searchItemInfo).append(rankingHTML);

            htmlResult.append($searchItemAdditionalData);
        } else if (searchItemInfo.html() != '') {
            htmlResult.append(searchItemInfo);
        } else if (rankingHTML.html() != '') {
            htmlResult.append(rankingHTML);
        }

        return htmlResult;
    }

    /**
     * @description Compare two result pages to see if there are similar
     * @param result1 Result page
     * @param result2 Result page
     * @returns {boolean} true - result pages are similar
     *                    false - result pages are not similar
     */
    function similarPage(result1, result2) {
        var toReturn = false;

        if (result1 === undefined || result2 === undefined) {
            return toReturn;
        }

        var pageTitle1 = result1.title;
        var pageShortDesc1 = result1.shortDescription;

        var pageTitle2 = result2.title;
        var pageShortDesc2 = result2.shortDescription;

        if (pageTitle1.trim() == pageTitle2.trim() && pageShortDesc1.trim() == pageShortDesc2.trim()) {
            toReturn = true;
        }

        return toReturn;
    }

    /**
     * @description Show similar results that are hidden by default
     */
    function showSimilarResults() {
        var parentLiElement = $(this).parents('li[id]');
        var currentResultId = parentLiElement.attr('id');

        $('[data-similarTo="' + currentResultId + '"]').toggle();
        $(this).toggleClass('expanded');
    }
});
