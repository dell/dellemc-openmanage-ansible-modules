define(["index", "options", "stemmer", "util"], function(index, options, stemmer, util) {
    /*

     David Cramer
     <david AT thingbag DOT net>

     Kasun Gajasinghe
     <kasunbg AT gmail DOT com>

     Copyright © 2008-2012 Kasun Gajasinghe, David Cramer

     Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

     1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

     2. Except as contained in this notice, the names of individuals credited with contribution to this software shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization from the individuals in question.

     3. Any stylesheet derived from this Software that is publicly distributed will be identified with a different name and the version strings in any derived Software will be changed so that no possibility of confusion between the derived package and this Software will exist.

     Warranty: THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL DAVID CRAMER, KASUN GAJASINGHE, OR ANY OTHER CONTRIBUTOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

     */


    /*
     List of modifications added by the Oxygen Webhelp plugin:

     1. Make sure the space-separated words from the search query are
     passed to the search function searchSingleWord() in all cases (the
     total number of words can be less than or greater than 10 words).

     2. Accept as valid search words a sequence of two words separated
     by ':', '.' or '-'.

     3. Convert the search query to lowercase before executing the search.

     4. Do not omit words between angle brackets from the title of the
     search results.

     5. Normalize search results HREFs and add '#' for no-frames webhelp

     6. Keep custom footer in TOC after searching some text

     7. Accept as valid search words that contains only 2 characters

     */

    /**
     * Is set to true when the CJK tokenizer is used.
     * @type {boolean}
     */
    var useCJKTokenizing = false;

    /**
     * The map with indexed words.
     *
     * w[word] = topicID*score, topicID*score;
     */
    var w = {};

    /**
     * Array with excluded words from search.
     *
     * @type {[string]}
     */
    var excluded = [];

    /**
     * The search query used in search process, after it was filtered.
     */
    var realSearchQuery;

    /**
     * It is true when the user searches for a single word between quotes, like "flower".
     * In this case only this word will be displayed as search result.
     *
     * Note that it is not taken into consideration when stemming is activated.
     *
     * @type {boolean}
     */
    var singleWordExactMatch = false;

    /**
     * It is true when the search query seems to be a part of am URL or file path.
     * For this situation we will search using 'contains' method.
     *
     * @type {boolean}
     */
    var searchInsideFilePath = false;

    /**
     * It is true when original search expression contains boolean operators.
     *
     * @type {boolean}
     */
    var booleanSearch = false;

    /**
     * The default boolean search operator.
     * @type {string}
     */
    var defaultOperator = "or";


    /**
     * List of all known operators.
     * @type {string[]}
     */
    var knownOperators = ["and", "or", "not"];

    /**
     * A hashtable which maps stems to query words
     */
    var stemQueryMap = [];

    /**
     * A map that contains search results organized by categories.
     *
     * @type {}
     */
    var resultCategoriesMap = {};

    /**
     * The number of result categories already counted.
     *
     * @type {number}
     */
    var resultCategoriesCount = 0;

    /**
     * Arrays with file IDs that were already in search result.
     *
     * @type {Array}
     */
    var resultCategoriesMapFiles = [];

    /**
     * An object describing the search result. It contains a string with the search expression and a list with documents
     * where search terms were found.
     *
     * @param {string} searchExpression The search expression that belongs/represents this result.
     * It might be different from the initial search expression after stop words and invalid boolean operators were removed.
     * @param {[string]} The array with excluded words from initial search expression.
     * @param {string} originalSearchExpression The initial search expression.
     * @param {DocumentInfo[]} documents The array containing the search result grouped by topic/document.
     * @param {string} errorMsg The message returned by search when an error occurred. This message will be displayed to user.
     *
     * @constructor
     */
    function SearchResult(searchExpression, excluded, originalSearchExpression, documents, errorMsg) {
        this.searchExpression = searchExpression;
        this.excluded = excluded;
        this.documents = documents;
        this.originalSearchExpression = originalSearchExpression;
        this.error = errorMsg;
    }

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
     * @constructor
     */
    function DocumentInfo(topicID, relativePath, title, shortDescription, words, scoring) {
        this.topicID = topicID;
        this.relativePath = relativePath;
        this.title = title;
        this.shortDescription = shortDescription;
        this.words = words;
        this.scoring = scoring;
    }

    /**
     * This is the main function of the WH search library used to execute a search query.
     * The stop words are filtered.
     *
     * @param {String} searchQuery The search query
     * @return {SearchResult}The search result containing the search expression together with an arrays
     * of DocumentInfo objects.
     */
    function performSearchInternal(searchQuery) {
        util.debug("searchQuery", searchQuery);
        init();

        var searchQueryOrig = searchQuery;
        var initialSearchExpression = searchQuery;
        var phraseSearch = false;

        var indexerLanguage = options.getIndexerLanguage().toLowerCase();
        var useCJKTokenizing = !!(typeof indexerLanguage != "undefined" && (indexerLanguage == "zh" ||
            indexerLanguage == "zh-cn" ||
            indexerLanguage == "zh-tw" ||
            indexerLanguage == "zh-hk" ||
            indexerLanguage == "ja" ||
            indexerLanguage == "ja-jp" ||
            indexerLanguage == "ko-kr" ||
            indexerLanguage == "ko"));
        if (useCJKTokenizing && initialSearchExpression.length > 1) {
            var initialSearchExpressionNoSpaces = initialSearchExpression.replace(/\s+/g, '');
            var initialSearchExpressionSplitArray = [];

            splitString(initialSearchExpressionNoSpaces, initialSearchExpressionNoSpaces.length);

            initialSearchExpression = initialSearchExpressionSplitArray.join(" ");
            function splitString(str, pos) {
                for(var i = 0; i < pos-1; i++){
                    initialSearchExpressionSplitArray.push(str.substring(0, pos - i));
                }
                if (pos > 1) {
                    splitString(str.substring(1, pos), pos-1)
                }

            }
        }
        searchQuery = searchQuery.trim();
        if (searchQuery.length > 2 && !useCJKTokenizing) {
            var firstChar = searchQuery.charAt(0);
            var lastChar = searchQuery.charAt(searchQuery.length - 1);
            phraseSearch =
                (firstChar == "'" || firstChar == '"') &&
                (lastChar == "'" || lastChar == '"');
        }

        // Remove ' and " characters
        searchQuery = searchQuery.replace(/"/g, " ").replace(/'/g, " ")

        var errorMsg;
        try {
            realSearchQuery = preprocessSearchQuery(initialSearchExpression, phraseSearch);
        } catch (e) {
            errorMsg = e.message;
            util.debug(e);
        }
        util.debug("Search query after pre-process: ", realSearchQuery);
        if (realSearchQuery.trim().length != 0) {
            // Add the default boolean operator between words if it is missing
            searchQuery = normalizeQuery(realSearchQuery);

            var searchWordCount = 1;
            if (!useCJKTokenizing) {
                var sw = searchQuery.split(" ");
                searchWordCount = sw.length;
                singleWordExactMatch = phraseSearch && searchWordCount == 1;

                if (!singleWordExactMatch && !phraseSearch) {
                    searchInsideFilePath = isURLorFilePath(realSearchQuery);
                }
            }

            // Convert to RPN notation
            var rpnExpression = convertToRPNExpression(searchQuery);

            // Perform search with RPN expression
            var res = calculateRPN(rpnExpression);
            var sRes = res.value;

            if (searchWordCount == 1) {
                // single word search
                var doStem = options.getBoolean('use.stemming');
                if (!singleWordExactMatch && !doStem && !useCJKTokenizing) {
                    // Perform exact match first
                    singleWordExactMatch = true;
                    var exactMatchRes = calculateRPN(rpnExpression);
                    addSearchResultCategory(exactMatchRes.value);

                    // Add other results with lower priority
                    addSearchResultCategory(sRes);
                } else {
                    addSearchResultCategory(sRes);
                }

            } else {
                if (phraseSearch) {
                    sRes = filterResultsForPhraseSearch(res.value, realSearchQuery);
                    addSearchResultCategory(sRes);
                } else if (booleanSearch) {
                    groupResultsByWordCount(sRes);
                } else {
                    // Search criterion was not specified
                    var phraseSearchResult =
                        filterResultsForPhraseSearch(res.value, realSearchQuery);
                    addSearchResultCategory(phraseSearchResult);

                    groupResultsByWordCount(sRes);
                }
            }

            sRes = sortSearchResults();

            var docInfos = [];
            for (var i = 0; i < sRes.length; i++) {
                var cDoc = sRes[i];

                var topicInfo = index.fil[cDoc.filenb];

                if (topicInfo == undefined) {
                    warn("There is no definition for topic with ID ", cDoc.filenb);
                    continue;
                }

                var pos1 = topicInfo.indexOf("@@@");
                var pos2 = topicInfo.lastIndexOf("@@@");
                var relPath = topicInfo.substring(0, pos1);

                // EXM-27709 START
                // Display words between '<' and '>' in title of search results.
                var topicTitle = topicInfo.substring(pos1 + 3, pos2)
                    .replace(/</g, "&lt;").replace(/>/g, "&gt;");
                // EXM-27709 END
                var topicShortDesc = topicInfo.substring(pos2 + 3, topicInfo.length);

                var wordsStrArray = [];
                for (var k in cDoc.wordsList) {
                    wordsStrArray.push(cDoc.wordsList[k].word);
                }

                var docInfo =
                    new DocumentInfo(
                        cDoc.filenb,
                        relPath,
                        topicTitle,
                        topicShortDesc,
                        wordsStrArray,
                        cDoc.scoring);

                docInfos.push(docInfo);
            }
        }
        // Filter expression to cross site scripting possibility
        initialSearchExpression = filterOriginalSearchExpression(initialSearchExpression);
        var searchResult = new SearchResult(initialSearchExpression, excluded, searchQueryOrig, docInfos, errorMsg);
        return searchResult;
    }

    /**
     * Initialize the library for search.
     */
    function init() {
        searchInsideFilePath = false;
        excluded = [];
        realSearchQuery = "";
        singleWordExactMatch = false;
        booleanSearch = false;
        resultCategoriesMap = {};
        resultCategoriesCount = 0;
        resultCategoriesMapFiles = [];
    }

    /**
     * Add a search result category. This new added category has a lower priority.
     *
     * @param searchCategory The search results category.
     */
    function addSearchResultCategory(searchCategory) {
        // Filter results that was already registered
        /*info("************ addSearchResultCategory ", searchCategory);*/
        var filteredResults = [];
        for (var si = 0; si < searchCategory.length; si++) {
            // Make sure that score is greater than 0
            searchCategory[si].scoring = Math.max(1, searchCategory[si].scoring);

            if (resultCategoriesMapFiles.indexOf(searchCategory[si].filenb) == -1) {
                filteredResults.push(searchCategory[si]);

                resultCategoriesMapFiles.push(searchCategory[si].filenb);
            }
        }

        if (filteredResults.length > 0) {
            resultCategoriesMap[resultCategoriesCount++] = filteredResults;
        }
    }

    /**
     * Scale scoring to be between 0 and 100.
     *
     * @param {[ResultPerFile]} sortResult The sort result to scale.
     */
    function scaleSortResultScoring(sortResult) {
        var maxScore = 0;
        for (var i = 0; i < sortResult.length; i++) {
            maxScore = Math.max(maxScore, sortResult[i].scoring);
        }

        if (maxScore != 0) {
            var ratio = 99 / maxScore;

            for (var i = 0; i < sortResult.length; i++) {
                var s = Math.ceil(sortResult[i].scoring * ratio);

                var s = Math.min(99, s);
                sortResult[i].scoring = s;
            }
        }
    }

    function sortSearchResults() {
        var result = [];

        var keys = [];
        for (var prop in resultCategoriesMap) {
            keys.push(prop);
        }
        keys.sort();

        var catNumber = keys.length;
        for (var k = 0; k < keys.length; k++) {
            var r = resultCategoriesMap[k];


            scaleSortResultScoring(r);


            r.sort(function (first, second) {
                return -(first.scoring - second.scoring);
            });

            for (var ri = 0; ri < r.length; ri++) {
                r[ri].scoring = r[ri].scoring + ((catNumber - 1 - k) * 100);
            }

            result = result.concat(r);
        }

        /*info("final result:", result);*/
        return result;
    }

    /**
     * Filter results for phrase search.
     *
     * @param {[ResultPerFile]} resPerFileArray The array with search results to be filtered.
     * @param realSearchQuery The search query.
     * @returns {Array} The filtered array.
     */
    function filterResultsForPhraseSearch(resPerFileArray, realSearchQuery) {
        var searchWords = realSearchQuery.split(" ");

        var doStem = options.getBoolean('use.stemming');
        var fResult = [];
        // Iterate over all results
        for (var i = 0; i < resPerFileArray.length; i++) {
            // Test if number of words are the same
            if (searchWords.length == resPerFileArray[i].wordsList.length) {

                // Test if words are the same
                var sameWords = true;
                for (var j = 0; j < resPerFileArray[i].wordsList.length; j++) {
                    var sj = searchWords[j];
                    if (typeof stemmer != "undefined" && doStem) {
                        sj = stemmer(sj);
                    }
                    sj = sj.toLowerCase();

                    if (sj != resPerFileArray[i].wordsList[j].word) {
                        sameWords = false;
                        break;
                    }

                }

                if (sameWords) {
                    // Test if indices are consecutive

                    var firstWordIndices = resPerFileArray[i].wordsList[0].indices;

                    for (var fi in firstWordIndices) {
                        var cidx = parseInt(firstWordIndices[fi], 32);
                        if (cidx == -1) {
                            continue;
                        }

                        var consecutiveIndices = true;
                        // Test if next words indices are consecutive
                        for (var ii = 1; ii < resPerFileArray[i].wordsList.length; ii++) {

                            var nextIndices = resPerFileArray[i].wordsList[ii].indices;

                            var nextIdxFound = false;
                            for (var nIdx in nextIndices) {
                                var cRes = parseInt(nextIndices[nIdx], 32);

                                if (cRes != -1 && cidx == cRes - 1) {
                                    cidx = cRes;
                                    nextIdxFound = true;
                                    break;
                                }
                            }

                            if (!nextIdxFound) {
                                consecutiveIndices = false;
                                break;
                            }
                        }

                        if (consecutiveIndices) {
                            fResult.push(resPerFileArray[i]);
                            break;
                        }
                    }
                }
            }
        }
        return fResult;
    }

    /**
     * Filter the original search query to avoid cross site scripting possibility.
     *
     * @param {string} searchTextField The search query to process.
     * @returns {string} The filtered search query.
     */
    function filterOriginalSearchExpression(searchTextField) {
        // Eliminate the cross site scripting possibility.
        searchTextField = searchTextField.replace(/</g, " ")
            .replace(/>/g, " ")
            .replace(/"/g, " ")
            .replace(/'/g, " ")
            .replace(/=/g, " ")
            .replace(/0\\/g, " ")
            .replace(/\\/g, " ")
            .replace(/\//g, " ")
            .replace(/  +/g, " ");

        /*  START - EXM-20414 */
        searchTextField =
            searchTextField.replace(/<\//g, "_st_").replace(/\$_/g, "_di_").replace(/%2C|%3B|%21|%3A|@|\/|\*/g, " ").replace(/(%20)+/g, " ").replace(/_st_/g, "</").replace(/_di_/g, "%24_");
        /*  END - EXM-20414 */

        searchTextField = searchTextField.replace(/  +/g, " ");
        searchTextField = searchTextField.replace(/ $/, "").replace(/^ /, " ");

        return searchTextField;
    }


    /**
     * Pre-process the search query before it is used as search expression. It removes the stop words.
     *
     * @param {string} query The search query to process.
     * @param {boolean} phraseSearch True if phrase search was detected.
     * @returns {string} The processing result.
     */
    function preprocessSearchQuery(query, phraseSearch) {
        var searchTextField = trim(query);

        /**
         * Validate brackets
         */
        var openBracket = [],
            closedBracket = [];

        var idx = 0, oIndex;
        while (query.indexOf("(", idx) !== -1) {
            idx = query.indexOf("(", idx);
            openBracket.push(idx);
            idx++;
        }

        idx = 0;
        while (query.indexOf(")", idx) !== -1) {
            idx = query.indexOf(")", idx);
            closedBracket.push(idx);
            idx++;
        }

        if (openBracket.length != closedBracket.length) {
            throw new Error("Invalid expression!");
        } else {
            while (oIndex = openBracket.shift()) {
                var cIndex = closedBracket.shift();
                if (oIndex > cIndex) {
                    throw new Error("Invalid expression!");
                }
            }
        }

        // Add a space between '(' or ')' and the real word
        searchTextField = searchTextField.replace(/\((\S*)/g, '( $1');
        searchTextField = searchTextField.replace(/\)(\S*)/g, ') $1');
        searchTextField = searchTextField.replace(/(\S*)\)/g, '$1 )');

        // EXM-39245 - Remove punctuation marks
        // w1,w2 -> w1 w2
        searchTextField = searchTextField.replace(/[,]/g, ' ');

        // w1. w2 -> w1 w2
        searchTextField = searchTextField.replace(/\s\./g, ' ');
        searchTextField = searchTextField.replace(/\.\s/g, ' ');

        // w1! w2 -> w1 w2
        searchTextField = searchTextField.replace(/\s!/g, ' ');
        searchTextField = searchTextField.replace(/!\s/g, ' ');

        // w1? w2 -> w1 w2
        searchTextField = searchTextField.replace(/\s\?/g, ' ');
        searchTextField = searchTextField.replace(/\?\s/g, ' ');

        var expressionInput = searchTextField;

        var wordsArray = [];
        var splitExpression = expressionInput.split(" ");

        // Exclude/filter stop words
        for (var t in splitExpression) {
            var cw = splitExpression[t].toLowerCase();
            if (cw.trim().length == 0) {
                // Empty string
                continue;
            }

            var isParenthesis =
                "(" == cw || ")" == cw;

            if (contains(knownOperators, cw)) {
                // Boolean operators are excluded from phrase search
                if (phraseSearch) {
                    excluded.push(cw);
                } else {
                    wordsArray.push(cw);
                }
            } else if (isParenthesis) {
                // Paranthesis are excluded from phrase search
                if (phraseSearch) {
                    excluded.push(cw);
                } else {
                    wordsArray.push(cw);
                }
            } else if (contains(index.stopWords, cw)) {
                // Exclude stop words
                excluded.push(cw);
            } else {
                wordsArray.push(cw);
            }
        }

        expressionInput = wordsArray.join(" ");

        realSearchQuery = expressionInput;
        return expressionInput.trim();
    }

    /**
     * Group the search results by word count.
     *
     * @param {[ResultPerFile]} searchResults The search results to be grouped.
     */
    function groupResultsByWordCount(searchResults) {
        var resultsByWordCount = {};

        for (var sri = 0; sri < searchResults.length; sri++) {
            var csr = searchResults[sri];

            var wc = csr.wordsList.length;
            if (resultsByWordCount[wc] == undefined) {
                resultsByWordCount[wc] = [];
            }
            resultsByWordCount[wc].push(csr);
        }
        /*info("Results by words count:", resultsByWordCount);*/

        var keys = [];
        for (var prop in resultsByWordCount) {
            keys.push(prop);
        }
        keys.sort();
        /*info("Sorted keys", keys);*/

        for (var k = keys.length - 1; k >= 0; k--) {
            var ck = keys[k];

            addSearchResultCategory(resultsByWordCount[ck]);
        }
    }

    /**
     * @description Combine two selectors into one
     * e.g: "and or" => "or"
     * @param {String} op1 Operator one
     * @param {String} op2 Operator two
     * @returns {String} Resulted operator
     */
    function combineOperators(op1, op2) {
        if (op1 == op2) {
            return op1;
        }

        if (op1 == "not" || op2 == "not") {
            return "not";
        }

        if (op1 == "or" || op2 == "or") {
            return "or";
        }
    }

    /**
     * @param word Word to check if is an known operator or not
     * @returns {boolean} TRUE if searched word is a known operator
     *                    FALSE otherwise
     */
    function isKnownOperator(word) {
        return inArray(word, knownOperators);
    }

    /**
     * @description Normalize query so that we have an operator between each two adjacent search terms. We'll add the defaultOperator if the
     * operator is missing.
     * e.g: If the defaultOperator is "and" the "iris flower" query will be "iris and flower"
     *
     * @param {String} query Search query
     * @return {String} Normalized query
     */
    function normalizeQuery(query) {
        util.debug("normalizeQuery(" + query + ")");
        var toReturn = [];

        // Remove whitespaces from the beginning and from the end of the expression
        query = query.toLowerCase().trim();
        // Consider "-" (dash) character to be "and" operator
        //query = query.replace(/-/g, ' and ');
        // Replace multiple spaces with a single space
        query = query.replace(/  +/g, ' ');
        // Remove space after left bracket
        query = query.replace(/\( /g, '(');
        // Remove space before right bracket
        query = query.replace(/ \)/g, ')');

        var queryParts = query.split(" ");
        for (var i = 0; i < queryParts.length; i++) {
            // Skip empty parts
            var currentWord = queryParts[i];
            if (currentWord == "") {
                continue;
            }

            var knownOperator = isKnownOperator(currentWord);
            booleanSearch = booleanSearch || knownOperator;
            if (toReturn.length == 0) {
                // First item in result should be a term, not an operator
                if (!knownOperator) {
                    toReturn.push(currentWord);
                }
            } else {
                // Combine multiple operators into one
                if (isKnownOperator(toReturn[toReturn.length - 1]) && knownOperator) {
                    toReturn[toReturn.length - 1] = combineOperators(toReturn[toReturn.length - 1], currentWord);
                }
                // Add default operator when no operator is specified
                if (!isKnownOperator(toReturn[toReturn.length - 1]) && !knownOperator) {
                    toReturn.push(defaultOperator);
                    toReturn.push(currentWord);
                }
                // Add operator after term
                if (!isKnownOperator(toReturn[toReturn.length - 1]) && knownOperator) {
                    toReturn.push(currentWord);
                }
                // Add term after operator
                if (isKnownOperator(toReturn[toReturn.length - 1]) && !knownOperator) {
                    toReturn.push(currentWord);
                }
            }
        }

        // Remove the last operators from the list
        for (i = toReturn.length - 1; i >= 0; i--) {
            if (isKnownOperator(toReturn[i])) {
                toReturn.pop();
            } else {
                break;
            }
        }

        return toReturn.join(" ");
    }

    /**
     * @description Convert search expression from infix notation to reverse polish notation (RPN): iris and flower => iris flower and
     * @param {string} search Search expression to be converted. e.g.: iris and flower or (gerbera not salvia)
     * @return {String} Search expression in RPN notation
     */
    function convertToRPNExpression(search) {
        util.debug("convertToRPNExpression(" + search + ")");
        var stringToStore = "";
        var stack = [];
        var item = "";
        var items = [];
        for (var i = 0; i < search.length; i++) {
            if (search[i] != " " && search[i] != "(" && search[i] != ")") {
                item += search[i];
            }
            if (search[i] == " ") {
                if (item != "") {
                    items.push(item);
                    item = "";
                }
            }
            if (search[i] == "(") {
                if (item != "") {
                    items.push(item);
                    items.push("(");
                    item = "";
                } else {
                    items.push("(");
                }
            }
            if (search[i] == ")") {
                if (item != "") {
                    items.push(item);
                    items.push(")");
                    item = "";
                } else {
                    items.push(")");
                }
            }
        }

        if (item != "") {
            items.push(item);
        }

        for (i = 0; i < items.length; i++) {
            if (isTerm(items[i])) {
                stringToStore += items[i] + " ";
            }
            if (inArray(items[i], knownOperators)) {
                while (stack.length > 0 && inArray(stack[stack.length - 1], knownOperators)) {
                    stringToStore += stack.pop() + " ";
                }
                stack.push(items[i]);
            } else if (items[i] == "(") {
                stack.push(items[i]);
            } else if (items[i] == ")") {
                var popped = stack.pop();
                while (popped != "(") {
                    stringToStore += popped + " ";
                    popped = stack.pop();
                }
            }
        }

        while (stack.length > 0) {
            stringToStore += stack.pop() + " ";
        }

        return stringToStore.trim();
    }

    /**
     * @description Compute results from a RPN expression
     * @param {string} rpn Expression in Reverse Polish notation
     * @return {Page} An object that contains the search result.
     */
    function calculateRPN(rpn) {
        util.debug("calculate(" + rpn + ")");
        var lastResult1, lastResult2;
        var rpnTokens = trim(rpn);
        rpnTokens = rpnTokens.split(' ');
        var result;

        var stackResults = [];

        var realSearchWords = [];
        for (var i = 0; i < rpnTokens.length; i++) {
            var token = rpnTokens[i];

            if (isTerm(token)) {
                result = searchSingleWord(token);

                util.debug(token, " -- single word search result -- ", result);
                realSearchWords.push(token);

                if (result.length > 0) {
                    stackResults.push(new BooleanSearchOperand(result));
                } else {
                    stackResults.push(new BooleanSearchOperand([]));
                }
            } else {
                switch (token) {
                    case "and":
                        // debug("Implement AND operator");
                        lastResult2 = stackResults.pop();
                        lastResult1 = stackResults.pop();

                        if (lastResult1.value == undefined || !inArray(token, knownOperators)) {
                            util.debug("Error in calculateRPN(string) Method!");
                        } else {
                            stackResults.push(lastResult1.and(lastResult2));
                        }
                        break;
                    case "or":
                        lastResult2 = stackResults.pop();
                        lastResult1 = stackResults.pop();
                        if (lastResult1.value == undefined || !inArray(token, knownOperators)) {
                            util.debug("Error in calculateRPN(string) Method!");
                        } else {
                            stackResults.push(lastResult1.or(lastResult2));
                        }
                        break;
                    case "not":
                        lastResult2 = stackResults.pop();
                        lastResult1 = stackResults.pop();
                        if (lastResult1.value == undefined || !inArray(token, knownOperators)) {
                            util.debug("Error in calculateRPN(string) Method!");
                        } else {
                            stackResults.push(lastResult1.not(lastResult2));
                        }
                        break;
                    default:
                        util.debug("Error in calculateRPN(string) Method!");
                        break;
                }
            }
        }

        realSearchQuery = realSearchWords.join(" ");
        return stackResults[0];
    }

    /**
     * Tests if a given string is a valid search term or not.
     *
     * @param {string} string String to look for in the known operators list
     * @return {boolean} TRUE if the search string is a search term
     *                   FALSE if the search string is not a search term
     */
    function isTerm(string) {
        return !inArray(string, knownOperators) && string.indexOf("(") == -1 && string.indexOf(")") == -1;
    }

    /**
     * @description Search for an element into an array
     * @param needle Searched element
     * @param haystack Array of elements
     * @return {boolean} TRUE if the searched element is part of the array
     *                   FALSE otherwise
     */
    function inArray(needle, haystack) {
        var length = haystack.length;
        for (var i = 0; i < length; i++) {
            if (haystack[i] == needle) return true;
        }

        return false;
    }

    /**
     * Search for a single word/term.
     *
     * @param {String} wordToFind A single search term to search for.
     * @return {[ResultPerFile]} Array with the resulted pages and indices.
     */
    function searchSingleWord(wordToFind) {
        util.debug('searchSingleWord("' + wordToFind + '")');

        wordToFind = trim(wordToFind);
        wordToFind = wordToFind.toLowerCase();

        var txt_wordsnotfound = "";
        var wordsList = [wordToFind];
        util.debug('words from search:', wordsList);

        var indexerLanguage = options.getIndexerLanguage();
        // set the tokenizing method
        useCJKTokenizing = !!(typeof indexerLanguage != "undefined" && (indexerLanguage == "zh" || indexerLanguage == "ko"));
        //If Lucene CJKTokenizer was used as the indexer, then useCJKTokenizing will be true. Else, do normal tokenizing.
        // 2-gram tokenizing happens in CJKTokenizing,
        // If doStem then make tokenize with Stemmer
        //var finalArray;

        /**
         * data initialisation
         */
        var finalWordsList = []; // Array with the words to look for after removing spaces
        var doStem = options.getBoolean('use.stemming');
        if (doStem) {
            if (useCJKTokenizing) {
                // Array of words
                finalWordsList = cjkTokenize(wordsList);
            } else {
                // Array of words
                finalWordsList = tokenize(wordsList);
            }
        } else if (useCJKTokenizing) {
            // Array of words
            finalWordsList = cjkTokenize(wordsList);
            util.debug('CJKTokenizing, finalWordsList: ' + finalWordsList);
        } else {
            finalWordsList = [wordToFind];
        }

        // Add the words that start with the searched words.
        if (!useCJKTokenizing) {
            /**
             * Compare with the indexed words (in the w[] array), and push words that are in it to tempTab.
             */
            var tempTab = [];

            var wordsArray = '';
            for (var t in finalWordsList) {
                if (!contains(index.stopWords, finalWordsList[t])) {
                    if (doStem || finalWordsList[t].toString().length == 2) {
                        if (index.w[finalWordsList[t].toString()] == undefined) {
                            txt_wordsnotfound += finalWordsList[t] + " ";
                        } else {
                            tempTab.push(finalWordsList[t]);
                        }
                    } else {
                        var searchedValue = finalWordsList[t].toString();
                        var listOfWordsStartWith = searchedValue + ",";
                        if (!singleWordExactMatch) {
                            if (searchInsideFilePath) {
                                listOfWordsStartWith = wordsContains(searchedValue);
                            } else {
                                listOfWordsStartWith = wordsStartsWith(searchedValue);
                            }

                        }

                        if (listOfWordsStartWith != undefined) {
                            listOfWordsStartWith = listOfWordsStartWith.substr(0, listOfWordsStartWith.length - 1);
                            wordsArray = listOfWordsStartWith.split(",");
                            for (var i in wordsArray) {
                                tempTab.push(wordsArray[i]);
                            }
                        }
                    }
                }
            }
            finalWordsList = tempTab;
            finalWordsList = removeDuplicate(finalWordsList);
        }

        var fileAndWordList = [];
        if (finalWordsList.length) {
            fileAndWordList = searchStartWith(finalWordsList, wordToFind);
        }

        return fileAndWordList;
    }

// Return true if "word" value is an element of "arrayOfWords"
    function contains(arrayOfWords, word) {
        var found = false;

        for (var w in arrayOfWords) {
            if (arrayOfWords[w] === word) {
                found = true;
                break;
            }
        }

        return found;
    }

// Look for elements that start with searchedValue.
    function wordsStartsWith(searchedValue) {
        var toReturn = '';
        for (var sv in index.w) {
            if (sv.toLowerCase().indexOf(searchedValue.toLowerCase()) == 0) {
                toReturn += sv + ",";
            }
        }
        return toReturn.length > 0 ? toReturn : undefined;
    }

// Look for indexed words that contains the searchedValue.
    function wordsContains(searchedValue) {
        var toReturn = '';
        for (var sv in index.w) {
            if (sv.toLowerCase().indexOf(searchedValue.toLowerCase()) != -1) {
                toReturn += sv + ",";
            }
        }
        return toReturn.length > 0 ? toReturn : undefined;
    }

    function tokenize(wordsList) {
        util.debug('tokenize(' + wordsList + ')');
        var stemmedWordsList = []; // Array with the words to look for after removing spaces
        var cleanwordsList = []; // Array with the words to look for
        var doStem = options.getBoolean('use.stemming');
        for (var j in wordsList) {
            var word = wordsList[j];
            if (typeof stemmer != "undefined" && doStem) {
                var s = stemmer(word);
                util.debug(word, " -stem- ", s);
                stemQueryMap[s] = word;
            } else {
                stemQueryMap[word] = word;
            }
        }

        //stemmedWordsList is the stemmed list of words separated by spaces.
        for (var t in wordsList) {
            if (wordsList.hasOwnProperty(t)) {
                wordsList[t] = wordsList[t].replace(/(%22)|^-/g, "");
                if (wordsList[t] != "%20") {
                    cleanwordsList.push(wordsList[t]);
                }
            }
        }

        if (typeof stemmer != "undefined" && doStem) {
            //Do the stemming using Porter's stemming algorithm
            for (var i = 0; i < cleanwordsList.length; i++) {
                var stemWord = stemmer(cleanwordsList[i]);
                stemmedWordsList.push(stemWord);
            }
        } else {
            stemmedWordsList = cleanwordsList;
        }
        return stemmedWordsList;
    }

//Invoker of CJKTokenizer class methods.
    function cjkTokenize(wordsList) {
        var allTokens = [];
        var notCJKTokens = [];
        util.debug('in cjkTokenize(), wordsList: ', wordsList);
        for (var j = 0; j < wordsList.length; j++) {
            var word = wordsList[j];
            util.debug('in cjkTokenize(), next word: ', word);
            if (getAvgAsciiValue(word) < 127) {
                notCJKTokens.push(word);
            } else {
                util.debug('in cjkTokenize(), use CJKTokenizer');
                var tokenizer = new CJKTokenizer(word);
                var tokensTmp = tokenizer.getAllTokens();
                allTokens = allTokens.concat(tokensTmp);
                util.debug('in cjkTokenize(), found new tokens: ', allTokens);
            }
        }
        allTokens = allTokens.concat(tokenize(notCJKTokens));
        return allTokens;
    }

//A simple way to determine whether the query is in english or not.
    function getAvgAsciiValue(word) {
        var tmp = 0;
        var num = word.length < 5 ? word.length : 5;
        for (var i = 0; i < num; i++) {
            if (i == 5) break;
            tmp += word.charCodeAt(i);
        }
        return tmp / num;
    }

//CJKTokenizer
    function CJKTokenizer(input) {
        this.input = input;
        this.offset = -1;
        this.tokens = [];
        this.incrementToken = incrementToken;
        this.tokenize = tokenize;
        this.getAllTokens = getAllTokens;
        this.unique = unique;

        function incrementToken() {
            if (this.input.length - 2 <= this.offset) {
                return false;
            } else {
                this.offset += 1;
                return true;
            }
        }

        function tokenize() {
            return this.input.substring(this.offset, this.offset + 2);
        }

        function getAllTokens() {
            while (this.incrementToken()) {
                var tmp = this.tokenize();
                this.tokens.push(tmp);
            }
            return this.unique(this.tokens);
        }

        function unique(a) {
            var r = [];
            o:for (var i = 0, n = a.length; i < n; i++) {
                for (var x = 0, y = r.length; x < y; x++) {
                    if (r[x] == a[i]) continue o;
                }
                r[r.length] = a[i];
            }
            return r;
        }
    }


    /**
     * Array.unique( strict ) - Remove duplicate values
     *
     * @param array The array to search.
     * @returns {*} The array without duplicates.
     */
    function unique(array) {
        util.debug("unique(", array, ")");
        var a = [];
        var i;
        var l = array.length;

        if (array[0] != undefined) {
            a[0] = array[0];
        }
        else {
            return -1;
        }

        for (i = 1; i < l; i++) {
            if (indexof(a, array[i], 0) < 0) {
                a.push(array[i]);
            }
        }

        return a;
    }

    /**
     * Finds the index of an element in an array.
     *
     * @param array The array.
     * @param element The element to find.
     * @param begin The begin index.
     * @returns The index of the element or -1.
     */
    function indexof(array, element, begin) {
        for (var i = begin; i < array.length; i++) {
            if (array[i] == element) {
                return i;
            }
        }
        return -1;

    }

    /* end of Array functions */


    /**
     * Searches in the indexed words for the terms in words and sort the mathes by scoring.
     *
     * @param {Array} words - list of words to look for.
     * @param {String} searchedWord - search term typed by user
     * @return {Array} - the hashtable fileAndWordList
     */
    function searchStartWith(words, searchedWord) {
        if (words.length == 0 || words[0].length == 0) {
            return null;
        }

        // In generated js file we add scoring at the end of the word
        // Example word1*scoringForWord1,word2*scoringForWord2 and so on
        // Split after * to obtain the right values

        // Group the words by topicID -> {word, indices}
        var fileAndWordList = {};
        for (var t in words) {
            // get the list of the indices of the files.
            var topicIDAndScore = index.w[words[t]];

            if (topicIDAndScore != undefined) {
                var topicInfoArray = topicIDAndScore.split(",");

                //for each file (file's index):
                for (var t2 in topicInfoArray) {
                    var tmp = '';

                    var temp = topicInfoArray[t2].toString();
                    var idx = temp.indexOf('*');
                    if (idx != -1) {
                        var tid = temp.substring(0, idx);

                        // Extract word indices
                        var starLastIdx = temp.indexOf("*", idx + 1);
                        var wordIndices = [];
                        if (starLastIdx != -1) {
                            var indicesStr = temp.substr(starLastIdx + 1);
                            wordIndices = indicesStr.split('$');
                        }

                        if (fileAndWordList[tid] == undefined) {
                            fileAndWordList[tid] = [];
                        }

                        var wAndIdx = {
                            word: words[t],
                            indices: wordIndices
                        };

                        fileAndWordList[tid].push(wAndIdx);
                    } else {
                        warn("Unexpected writing format, '*' delimiter is missing.");
                    }
                }
            }
        }


        // An array with TopicIDAndWordList objects
        var tidWordsArray = [];
        for (t in fileAndWordList) {
            tidWordsArray.push(new TopicIDAndWordList(t, fileAndWordList[t]));
        }
        tidWordsArray = removeDerivates(tidWordsArray, searchedWord);

        // Compute the array with results per file
        var resultsPerFileArrays = [];
        for (t in tidWordsArray) {
            var cTopicIDAndWordList = tidWordsArray[t];

            var scoring =
                computeScoring(fileAndWordList[cTopicIDAndWordList.filesNo], cTopicIDAndWordList.filesNo);
            resultsPerFileArrays.push(
                new ResultPerFile(
                    cTopicIDAndWordList.filesNo,
                    cTopicIDAndWordList.wordList,
                    scoring));
        }

        // Sort by score
        resultsPerFileArrays.sort(function (a, b) {
            return b.scoring - a.scoring;
        });

        return resultsPerFileArrays;
    }

    /**
     * Remove derivatives words from the list of words with the original word.
     *
     * @param {[TopicIDAndWordList]} obj Array that contains results for searched words
     * @param {String} searchedWord search term typed by user
     * @return {Array} Clean array results without duplicated and derivatives words
     */
    function removeDerivates(obj, searchedWord) {

        var toResultObject = [];
        for (var i in obj) {
            var filesNo = obj[i].filesNo;
            var wordList = obj[i].wordList;

            // concat word results if word starts with the original word
            var wordIndicesMap = {};
            for (var j = 0; j < wordList.length; j++) {
                var w = wordList[j].word;
                if (searchInsideFilePath) {
                    if (w.indexOf(searchedWord) != -1) {
                        w = searchedWord;
                    }
                } else {
                    if (startsWith(w, searchedWord)) {
                        w = searchedWord;
                    }
                }

                if (wordIndicesMap[w] == undefined) {
                    wordIndicesMap[w] = wordList[j].indices;
                } else {
                    wordIndicesMap[w] = wordIndicesMap[w].concat(wordList[j].indices);
                }
            }

            var newWordsAray = [];
            for (var w in wordIndicesMap) {
                newWordsAray.push(
                    {
                        word: w,
                        indices: wordIndicesMap[w]
                    }
                );
            }

            toResultObject.push(new TopicIDAndWordList(filesNo, newWordsAray));
        }

        return toResultObject;
    }

    /**
     * Object to keep the topicID and a list of words that was found in that topic.
     *
     * @param filesNo The topic ID or file number.
     * @param {[obj]} wordList An array of {word, [idx]} objects.
     * @constructor
     */
    function TopicIDAndWordList(filesNo, wordList) {
        this.filesNo = filesNo;
        this.wordList = wordList;
    }


// Object.
// Add a new parameter - scoring.

    /**
     * An object containing the search result for a single topic.
     * Contains pointer to the topicID and the list of words found.
     *
     * @param filenb The topic ID or number.
     * @param {obj[]} wordsList The array with words separated.
     * The object has form: {word: "flower"; indices: {1, 5, 7}}
     * @param scoring The scoring associated with this topic.
     *
     * @constructor
     */
    function ResultPerFile(filenb, wordsList, scoring) {
        this.filenb = filenb;
        this.wordsList = wordsList;
        this.scoring = scoring;
    }

    /**
     * Compute score for one or more words for a given topic ID.
     *
     * @param words {[word: string, indices: [integer]]} The list with words separated by ','.
     * @param topicID {number} The topic ID.
     * @returns {number} The score for the given words.
     */
    function computeScoring(words, topicID) {
        var sum = 0;

        for (var jj = 0; jj < words.length; jj++) {
            var cWord = words[jj].word;
            // Check if the word was indexed
            if (index.w[cWord] !== undefined) {
                // w["flowering"]="1*5,3*7";
                var topicIDScoreArray = index.w[cWord].split(',');
                for (var ii = 0; ii < topicIDScoreArray.length; ii++) {
                    var tidAndScore = topicIDScoreArray[ii].split('*');
                    if (tidAndScore[0] == topicID) {
                        sum += parseInt(tidAndScore[1]);
                    }
                }
            }
        }
        return sum;
    }

    function compareWords(s1, s2) {
        var t1 = s1.split(',');
        var t2 = s2.split(',');
        if (t1.length == t2.length) {
            return 0;
        } else if (t1.length > t2.length) {
            return 1;
        } else {
            return -1;
        }
    }

// Remove duplicate values from an array
    function removeDuplicate(arr) {
        var r = [];
        o:for (var i = 0, n = arr.length; i < n; i++) {
            for (var x = 0, y = r.length; x < y; x++) {
                if (r[x] == arr[i]) continue o;
            }
            r[r.length] = arr[i];
        }
        return r;
    }

    function trim(str, chars) {
        util.debug("Trim a string... " + str);
        return ltrim(rtrim(str, chars), chars);
    }

    function ltrim(str, chars) {
        chars = chars || "\\s";
        return str.replace(new RegExp("^[" + chars + "]+", "g"), "");
    }

    function rtrim(str, chars) {
        chars = chars || "\\s";
        return str.replace(new RegExp("[" + chars + "]+$", "g"), "");
    }

    /**
     * PATCH FOR BOOLEAN SEARCH
     */

    /**
     * @description Object with resulted pages as array
     * @param {[ResultPerFile]}resPerFileArray Array that contains partial results
     * @constructor
     */
    function BooleanSearchOperand(resPerFileArray) {
        this.value = resPerFileArray;

        this.toString = function () {
            var stringResult = "";

            stringResult += "INDEX\t|\tfilenb\t|\tscoring\n";
            for (var i = 0; i < this.value.length; i++) {
                stringResult += i + ".\t\t|\t" + this.value[i].filenb + "\t\t|\t" + this.value[i].scoring + "\n";
            }

            return stringResult;
        };

        this.writeIDs = function () {
            var stringResult = "";

            for (var i = 0; i < this.value.length; i++) {
                stringResult += this.value[i].filenb + " | ";
            }

            return stringResult;
        };

        /**
         * Combine two search results using AND function.
         *
         * @param {BooleanSearchOperand} secondOperand The second boolean operand to combine with.
         * @returns {BooleanSearchOperand} The AND operation result.
         */
        this.and = function and(secondOperand) {
            if (typeof secondOperand == "undefined" || secondOperand == null) {
                return this;
            }
            var result = [];

            for (var x = 0; x < this.value.length; x++) {
                var found = false;
                for (var y = 0; y < secondOperand.value.length; y++) {
                    if (this.value[x].filenb == secondOperand.value[y].filenb) {
                        this.value[x].wordsList = this.value[x].wordsList.concat(secondOperand.value[y].wordsList);
                        this.value[x].scoring += secondOperand.value[y].scoring;
                        found = true;
                        break;
                    }
                }
                if (found) {
                    result.push(this.value[x]);
                }
            }

            this.value = result;

            return this;
        };

        /**
         * Conbine two search results using OR operator.
         *
         * @param {Pages} operand The second operand.
         * @returns {BooleanSearchOperand} The new operand after applying the OR operator.
         */
        this.or = function or(operand) {
            if (typeof operand == "undefined" || operand == null) {
                return this;
            }
            this.value = this.value.concat(operand.value);
            var result = [];

            for (var i = 0; i < this.value.length; i++) {
                var unique = true;
                for (var j = 0; j < result.length; j++) {
                    if (this.value[i].filenb == result[j].filenb) {
                        result[j].wordsList = result[j].wordsList.concat(this.value[i].wordsList);
                        var numberOfWords = result[j].wordsList.length;
                        result[j].scoring = this.value[i].scoring + result[j].scoring;
                        unique = false;
                        break;
                    }
                }
                if (unique) {
                    result.push(this.value[i]);
                }
            }

            this.value = result;

            return this;
        };

        this.not = function not(newArray) {
            if (typeof newArray == "undefined" || newArray == null) {
                return this;
            }
            var result = [];

            for (var x = 0; x < this.value.length; x++) {
                var found = false;
                for (var y = 0; y < newArray.value.length; y++) {
                    if (this.value[x].filenb == newArray.value[y].filenb) {
                        found = true;
                    }
                }
                if (!found) {
                    result.push(this.value[x]);
                }
            }

            this.value = result;

            return this;
        };
    }

    /**
     * Utility method to debug a message. By default delegated to the console.log, but it can be overwritten
     * by other scripts.
     *
     * @param args The list with arguments.
     */
    function warn() {
        var res = typeof console.log;
        if (res === "function") {
            console.warn(console, arguments);
        }
    }

    /**
     * Utility method to debug a message. By default delegated to the console.log, but it can be overwritten
     * by other scripts.
     *
     * @param args The list with arguments.
     */
    function info() {
        var res = typeof console.info;
        if (res === "function") {
            console.info.apply(console, arguments);
        }
    }


    // Return true if "word1" starts with "word2"
    function startsWith(word1, word2) {
        var prefix = false;
        if (word1 !== null && word2 !== null) {
            if (word2.length <= word1.length) {
                prefix = true;
                for (var i = 0; i < word2.length; i++) {
                    if (word1.charAt(i) !== word2.charAt(i)) {
                        prefix = false;
                        break;
                    }
                }
            }
        } else {
            if (word1 !== null) {
                prefix = true;
            }
        }
        return prefix;
    }

    /**
     * Detect if a search token seems to be an URL or file path.
     *
     * @param toTest The search expression.
     * @returns {boolean} True if the search query seems to be an URL or file path.
     */
    function isURLorFilePath(toTest) {
        var re = new RegExp('[\./\\\-:_]');
        return re.test(toTest);
    }

    return {
        performSearch: performSearchInternal
    }

});