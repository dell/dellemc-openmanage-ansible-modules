define(['util', 'jquery'], function(util, $) {
    $(document).ready(function () {
        var searchQuery = '';
        searchQuery = util.getParameter('searchQuery');
        searchQuery = searchQuery.trim();
        searchQuery = decodeURIComponent(searchQuery);
       
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
            } else {
                // Eliminate the post and pre spaces int he input to avoid DOM XSS Issue 
                // JIRA - IDPL-16125 Code change added by 986204 on 12/8/2021
           	 $('#textToSearch').val().trim();
            }
        });
    });
});
