/*This file was created by DELL GSD.
  This file is being included as per Mantis Issue: 11733: Modification of index.html to handle deeplinks*/

/*  Google Analytics */
var _gaq = _gaq || [];
       _gaq.push(['_setAccount', 'UA-36679013-1']);
       _gaq.push(['_trackPageview']);

(function() {
       var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
       ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();

function readCookie(name) {
       var nameEQ = name + "=";
       var ca = document.cookie.split(';');
       for(var i=0;i < ca.length;i++) {
              var c = ca[i];
              while (c.charAt(0)==' ') c = c.substring(1,c.length);
              if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
       };  // for i
       return null;
};  // readCookie();

function eraseCookie(name) { document.cookie = "page=; expires=Thu, 01 Jan 1970 00:00:01 GMT;"; };

