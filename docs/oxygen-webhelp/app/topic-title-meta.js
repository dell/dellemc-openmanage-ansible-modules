/*
This file can be used in further code enhancements when we are adding any code explicitly.

This file is added to the base line and as well at the dell plugins level 
to fix the CSP Issues reported.

Content Secure Policy issue states that any script source code should not be written explicitly 
inside the html files
but can be referenced the same with script file using src attribute in the script tag under header section 
each html or topic files.

JIRA Reference : IDPL-15117
Author: Shrinidhi H A (986204)


*/


$(document).ready(function() {
	var metaelement = $("[name=meta-topic-title]");
	var newTitle = $(metaelement).attr("content");
	if(newTitle){
		document.title = newTitle;
	}
});