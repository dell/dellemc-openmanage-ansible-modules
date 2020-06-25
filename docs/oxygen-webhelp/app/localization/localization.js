/*

    Oxygen WebHelp Plugin
    Copyright (c) 1998-2018 Syncro Soft SRL, Romania.  All rights reserved.

    */
define(["strings"], function (strings) {

    return {
        /**
         * get translated messages
         */
        getLocalization: function (localizationKey) {
            var toReturn = localizationKey;
            if ((localizationKey in strings)) {
                toReturn = strings[localizationKey];
            }
            return toReturn;
        }
    };
});