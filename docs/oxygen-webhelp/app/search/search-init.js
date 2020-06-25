define(['util', 'jquery'], function(util, $) {
    $(document).ready(function () {
        var searchQuery = '';
        searchQuery = util.getParameter('searchQuery');
        searchQuery = decodeURIComponent(searchQuery);
        searchQuery = searchQuery.replace(/\+/g, " ");
        if (searchQuery != '' && searchQuery !== undefined && searchQuery != 'undefined') {
            $('#textToSearch').val(searchQuery);
            $('#searchForm').submit();
        }
    });
});
