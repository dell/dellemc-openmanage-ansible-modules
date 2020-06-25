define(["options", "en_stemmer", "de_stemmer", "fr_stemmer"], function(options, en_stemmer, de_stemmer, fr_stemmer) {
    var indexerLang = options.getIndexerLanguage();
    if (indexerLang == 'en') {
        return en_stemmer;
    } else if (indexerLang == 'de') {
        return de_stemmer;
    } else if (indexerLang == 'fr') {
        return fr_stemmer;
    } else {
        // Do nothing
    }
});