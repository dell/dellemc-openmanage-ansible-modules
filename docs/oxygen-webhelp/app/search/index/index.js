define(["stopwords", "index-1", "index-2", "index-3", "htmlFileInfoList", "link2parent", "jquery"], function(stopwords, index1, index2, index3, fileInfoList, link2parent, $) {

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
        fil : fileInfoList,

        link2parent : link2parent

    };
});