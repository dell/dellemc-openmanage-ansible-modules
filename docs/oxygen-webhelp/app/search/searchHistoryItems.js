define(['util', 'jquery'], function(util, $) {
    /**
     * The maximum number of items kept in local history for a specific WH output.
     *
     * @type {number}
     */
    var HISTORY_ITEMS_MAX_COUNT = 30;

    /**
     * Test if a browser local storage is available.
     *
     * @returns {boolean} Returns true if local storage is available.
     */
    function localStorageAvailable() {
        try {
            var storage = window["localStorage"],
                x = '__storage_test__';
            storage.setItem(x, x);
            storage.removeItem(x);
            return true;
        }
        catch (e) {
            util.debug(e);
            return false;
        }
    }

    /**
     * @returns {string} Get the key to use for reading from local storage. It is unique for a WH output.
     */
    function getSearchHistoryKey() {
        var wh_root = $('meta[name=wh-path2root]').attr('content');
        if (wh_root == null || wh_root == undefined || wh_root.length == 0) {
            wh_root = "index.html";
        } else {
            wh_root += "index.html";
        }

        var wh_root_path = resolveRelativePath(wh_root);
        return wh_root_path + "_search_history_items";
    }

    /**
     * Resolve a relative path to the current browser location.
     *
     * @param relPath The relative path to resolve.
     * @returns {string} The resolved URL.
     */
    function resolveRelativePath(relPath) {
        var link = document.createElement("a");
        link.href = relPath;
        return (link.protocol + "//" + link.host + link.pathname + link.search + link.hash);
    }

    return {
        /**
         * Add a search query to the history.
         *
         * @param searchQuery The search query to add.
         */
        addSearchQueryToHistory: function (searchQuery) {
            util.debug("Add search query to history: ", searchQuery);
            if (localStorageAvailable()) {
                searchQuery = searchQuery.toLowerCase();
                var localStorageKey = getSearchHistoryKey();
                try {
                    var localStorageItems = window.localStorage.getItem(localStorageKey);
                    if (!localStorageItems) {
                        // Local storage is empty for the current WH output.
                        var hItemsArray = [];
                        hItemsArray.push(searchQuery);
                        var valToSave = JSON.stringify(hItemsArray);
                        util.debug("Save to local storage: ", valToSave)
                        window.localStorage.setItem(localStorageKey, valToSave);
                    } else {
                        // There are local storage items for current WH output
                        var lastSearchItemsArray = JSON.parse(localStorageItems);
                        var idx = lastSearchItemsArray.indexOf(searchQuery);
                        if (idx != -1) {
                            // Promote history item
                            util.debug("Promote history item:", lastSearchItemsArray);
                            lastSearchItemsArray.splice(idx, 1);
                        }

                        // Add first
                        lastSearchItemsArray.unshift(searchQuery);

                        // Ensure local history items  do not exceed the MAX limit
                        if (lastSearchItemsArray.length > HISTORY_ITEMS_MAX_COUNT) {
                            lastSearchItemsArray.splice(HISTORY_ITEMS_MAX_COUNT);
                        }

                        // Save to local storage.
                        var newVal = JSON.stringify(lastSearchItemsArray);
                        window.localStorage.setItem(localStorageKey, newVal);

                    }
                } catch (e) {
                    util.debug("Exception when trying to save to local storage: ", e);
                    window.localStorage.removeItem(localStorageKey);
                }

            } else {
                util.debug("Local storage is not available");
            }
        },

        /**
         * Get the search history items from local storage.
         *
         * @returns {Array} The array with search history items.
         */
        getHistorySearchItems: function () {
            var toRet = [];
            if (localStorageAvailable()) {
                var localStorageKey = getSearchHistoryKey();

                try {
                    var lastLocalStorage = window.localStorage.getItem(localStorageKey);
                    if (lastLocalStorage) {
                        // Convert to array
                        var lastSearchItemsArray = JSON.parse(lastLocalStorage);

                        if (Array.isArray(lastSearchItemsArray)) {
                            toRet = lastSearchItemsArray;
                        }
                    }
                } catch (e) {
                    util.debug("Exception when reading from local storage: ", e);
                    window.localStorage.removeItem(localStorageKey);
                }
            }

            return toRet;
        },

        /**
         * Remove from local storage a history item.
         *
         * @param historyItem The history item to remove.
         * @returns {boolean} True if item was removed.
         */
        removeSearchHistoryItem: function (historyItem) {
            var removed = false;
            if (localStorageAvailable()) {
                var localStorageKey = getSearchHistoryKey();

                try {
                    var lastLocalStorage = window.localStorage.getItem(localStorageKey);
                    if (lastLocalStorage) {
                        // Convert to array
                        var lastSearchItemsArray = JSON.parse(lastLocalStorage);

                        if (Array.isArray(lastSearchItemsArray)) {
                            historyItem = historyItem.toLowerCase();
                            var idx = lastSearchItemsArray.indexOf(historyItem);
                            if (idx != -1) {
                                // Remove from local storage
                                lastSearchItemsArray.splice(idx, 1);
                                var newVal = JSON.stringify(lastSearchItemsArray);
                                window.localStorage.setItem(localStorageKey, newVal);

                                removed = true;
                            }
                        }
                    }
                } catch (e) {
                    util.debug("Exception when removing from local storage: ", e);
                    window.localStorage.removeItem(localStorageKey);
                }
            }

            return removed;
        }
    }
});