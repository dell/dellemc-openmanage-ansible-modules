define(["stopwords", "index-1", "index-2", "index-3", "htmlFileInfoList", "jquery"], function(stopwords, index1, index2, index3, fileInfoList, $) {

    var words = $.extend({}, index1, index2, index3);

    return {
        /**
         * The object with indexed words.
         *
         * {"word" : "topicID*score, topicID*score"}
         */
        w : words,
        /**
         * Auto generated list of analyzer stop words that must be ignored by search.
         */
        stopWords : stopwords,

        /**
         * File info list.
         */
        fil : fileInfoList

    };
});