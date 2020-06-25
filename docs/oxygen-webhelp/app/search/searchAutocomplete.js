define(["keywords", "searchHistoryItems", "options", "jquery", "jquery.ui"], function(keywordsInfo, searchHistory, options, $) {

// Install search autocomplete

    $(document).ready(function () {
        if (options.getBoolean("webhelp.enable.search.autocomplete")) {
            var searchFunction = function (request, response) {
                var searchTerm = request.term.toLowerCase();

                // Get history proposals.
                var historyItems = getHistoryProposals(searchTerm);

                var titlePhrases = [];
                var phraseIds = [];

                var keywords = keywordsInfo.keywords;
                var ph = keywordsInfo.ph;
                var words = searchTerm.split(" ");
                var sameHi;
                // Iterate over words
                for (var wi = 0; wi < words.length; wi++) {
                    var cw = words[wi].trim();
                    if (cw.length > 0) {
                        // Iterate over keywords to find the ones that contains the word
                        var newPhraseIds = [];
                        for (var i = 0; i < keywords.length; i++) {
                            if (keywords[i].w.toLowerCase().indexOf(cw) == 0) {
                                // Word was found
                                var phIds = keywords[i].p;
                                for (var pj = 0; pj < phIds.length; pj++) {
                                    var pid = phIds[pj];

                                    if (wi == 0) {
                                        newPhraseIds.push(pid);
                                    } else {
                                        // Keep only phrase indices that contains all words
                                        if (phraseIds.indexOf(pid) != -1) {
                                            newPhraseIds.push(pid);
                                        }
                                    }
                                }
                            }
                        }
                        phraseIds = newPhraseIds;
                    }
                }

                if (phraseIds.length > 0) {
                    // Compute proposals from titles/keywords
                    for (var pi = 0; pi < phraseIds.length; pi++) {
                        var wIdx = ph[phraseIds[pi]];

                        var pStr = "";
                        for (var wi = 0; wi < wIdx.length; wi++) {
                            var word = keywords[wIdx[wi]].w;
                            if (wi == 0) {
                                word = word.charAt(0).toUpperCase() + word.substr(1);
                            }
                            pStr += word;

                            if (wi < wIdx.length - 1) {
                                pStr += " ";
                            }
                        }

                        // Test if items is already in history proposals
                        for (var i = 0; i < historyItems.length; i++) {
                            if (pStr.toLocaleLowerCase() == historyItems[i]) {
                                sameHi = true;
                                break;
                            }
                        }

                        if (sameHi == null) {
                            var hp = {
                                label: pStr.toLowerCase(),
                                value: pStr.toLowerCase(),
                                type: "title"
                            };
                            titlePhrases.push(hp);
                        }
                    }
                } else {
                    var lastWord = words[words.length - 1];
                    var beforeLastWord = request.term.substring(0, searchTerm.lastIndexOf(lastWord));

                    for (var i = 0; i < keywords.length; i++) {
                        if (keywords[i].w.toLowerCase().indexOf(cw) == 0) {
                            var proposal = beforeLastWord + keywords[i].w;

                            // Test if items is already in history proposals
                            for (var j = 0; j < historyItems.length; j++) {
                                if (proposal.toLocaleLowerCase() == historyItems[j]) {
                                    sameHi = true;
                                    break;
                                }
                            }

                            if (sameHi == null) {
                                var hp = {
                                    label: proposal.toLowerCase(),
                                    value: proposal.toLowerCase(),
                                    type: "keyword"
                                };

                                titlePhrases.push(hp);
                            }
                        }
                    }
                }

                var res = [];
                res = res.concat(historyItems);
                res = res.concat(titlePhrases);

                response(res);
            };

            // Uncomment the following code if you want to take into account the border radius of the search input
            /*
            var leftMargin = parseInt($("#textToSearch").css("border-bottom-left-radius"));
            var rightMargin = parseInt($("#textToSearch").css("border-bottom-right-radius"));
            */

            var autocompleteObj = $("#textToSearch").autocomplete({
                source: searchFunction,
                minLength: 3
                // Uncomment the following code if you want to take into account the border radius of the search input
                /*
                ,
                position: {my : "left+" + leftMargin + " top"}
                */
            });

            // Close autocomplete on ENTER
            $("#textToSearch").keydown(function (event) {
                if (event.which == 13) {
                    $("#textToSearch").autocomplete("close");
                    $("#searchForm").submit();
                }
            });

            var auObj = autocompleteObj.data("ui-autocomplete");

            // Set width of the autocomplete area
            // Uncomment the following code if you want to take into account the border radius of the search input
            /*
            auObj._resizeMenu = function(){
                this.menu.element.outerWidth( parseInt($("#textToSearch").outerWidth()) - leftMargin - rightMargin );
            };
            */

            // Install a renderer
            auObj._renderItem = function (ul, item) {
                // Text to search
                var tts = $("#textToSearch").val();

                tts = tts.toLowerCase();
                var words = tts.split(" ");

                /*console.log("Render item:", item);*/

                var proposal = item.label;

                // Highlight words from search query
                var pw = proposal.split(" ");
                var newProposal = "";
                for (var pwi = 0; pwi < pw.length; pwi++) {
                    var cpw = pw[pwi];
                    if (cpw.trim().length > 0) {

                        // Iterate over words
                        var added = false;
                        for (var wi = 0; wi < words.length; wi++) {
                            var w = words[wi].trim();
                            if (w.length > 0) {
                                // Iterate over keywords to find the ones
                                // Highlight the text to search

                                try {
                                    w = w.replace("\\", "\\\\")
                                        .replace(")", "\\)")
                                        .replace("(", "\\(");
                                    var cpwh = cpw.replace(
                                        new RegExp("(" + w + ")", 'i'),
                                        "<span class='search-autocomplete-proposal-hg'>$1</span>");
                                } catch (e) {
                                    debug(e);
                                }

                                if (cpwh != cpw) {
                                    newProposal += cpwh;
                                    added = true;
                                    break;
                                }
                            }
                        }

                        if (!added) {
                            newProposal += cpw;
                        }

                        if (pwi < pw.length - 1) {
                            newProposal += " ";
                        }
                    }
                }

                var icon = "&nbsp;";
                if (item.type == 'history') {
                    icon = "h";
                }
                var proposalIcon =
                    $("<span>", {
                        class: "search-autocomplete-proposal-icon " + item.type,
                        html: icon
                    });

                // span with proposal label
                var proposalLabel =
                    $("<span>", {
                        class: "search-autocomplete-proposal-label",
                        "data-value": item.value,
                        html: newProposal
                    });

                // span with remove from history
                var removeButton;
                if (item.type == 'history') {
                    removeButton =
                        $("<span>", {
                            class: "search-autocomplete-proposal-type-history",
                            html: "<a data-value='" + item.value + "' class='glyphicon glyphicon-remove' />"
                        });
                    $(removeButton).find("a").on("click", function (event) {
                        removeHistoryItem(this);

                        // Do not close the menu
                        event.preventDefault();
                        event.stopPropagation();

                        return false;
                    });
                }

                var li = $("<li>", {
                    class: "ui-menu-item",
                    "data-value": item.value
                });
                var divWrapper = $("<div>", {
                    class: "ui-menu-item-wrapper"
                });
                li.append(divWrapper);
                divWrapper.append(proposalIcon).append(proposalLabel);

                if (removeButton != null) {
                    divWrapper.append(removeButton);
                }

                // If a search suggestion is chosen the form is submitted
                li.find(".ui-menu-item-wrapper").on("click", function (event) {
                    $("#textToSearch").val($(this).find(".search-autocomplete-proposal-label").attr('data-value'));
                    $("#searchForm").submit();
                });

                return li.appendTo(ul);
            };

            $(window).resize(function () {
                var autocompleteObj = $("#textToSearch").autocomplete("instance");
                autocompleteObj.search();
            });
        }
    });

    /**
     * Remove from local storage a history item.
     *
     * @param hi The renderer element.
     * @returns {boolean}
     */
    function removeHistoryItem(hi) {

        var historyItem = hi.getAttribute("data-value");
        var removed = searchHistory.removeSearchHistoryItem(historyItem);

        // Change label
        if (removed) {
            $(hi).attr("class", "glyphicon glyphicon-ok");
            $(hi).parents("div").find(".search-autocomplete-proposal-label").addClass("removed-from-history");
        }

        // Do not close the menu
        event.preventDefault();
        event.stopPropagation();
        return false;
    }

    /**
     * Compute search proposals from history items.
     *
     * @param searchQuery  The search query.
     * @returns {Array} The array with search proposals.
     */
    function getHistoryProposals(searchQuery) {
        var toRet = [];
        var historyItems = searchHistory.getHistorySearchItems();

        if (historyItems != null) {
            var words = searchQuery.split(" ");

            for (var i = 0; i < historyItems.length; i++) {
                /*console.log("History item", historyItems[i]);*/
                // Test if history item match the serch query
                if (matchSearchHistoryItem(historyItems[i], words)) {
                    var hp = {
                        label: historyItems[i],
                        value: historyItems[i],
                        type: "history"
                    };
                    toRet.push(hp);
                } else {
                    /*console.log("History item does not match...");*/
                }
            }
        }

        return toRet;
    }

    /**
     * Test if a history item match all words from search query.
     *
     * @param historyPhrase The history phrase.
     * @param words The list with words from search query.
     * @returns {boolean} True if history item matches the search words.
     */
    function matchSearchHistoryItem(historyPhrase, words) {
        // Iterate over words

        var historyWords = historyPhrase.split(" ");
        var allWordsMatch = true;

        for (var wi = 0; wi < words.length && allWordsMatch; wi++) {
            var cw = words[wi].trim();

            if (cw.length > 0) {
                // Iterate over keywords to find the ones that contains the word
                var wordFound = false;
                for (var i = 0; i < historyWords.length; i++) {
                    if (historyWords[i].toLowerCase().indexOf(cw.toLowerCase()) == 0) {
                        wordFound = true;
                        break;
                    }
                }

                allWordsMatch = allWordsMatch && wordFound;
            }
        }

        return allWordsMatch;
    }
});