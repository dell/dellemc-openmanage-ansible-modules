define(['util', 'jquery'], function(util, $) {
    $(document).ready(function () {
        var searchQuery = '';
        searchQuery = util.getParameter('searchQuery');
        searchQuery = decodeURIComponent(searchQuery);
        searchQuery = searchQuery.replace(/\+/g, " ");
        if (searchQuery.trim() != '' && searchQuery !== undefined && searchQuery != 'undefined') {
            $('#textToSearch').val(searchQuery);
            $('#searchForm').submit();
        }
        
        $('#searchForm').on('submit', function(event){
            util.debug('submit form....');
            if ($('#textToSearch').val().trim()=='') {
                event.preventDefault();
                event.stopPropagation();

                return false;
            }
        });
    });
});
