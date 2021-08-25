/**
 * If an old URL is given, redirect to the corresponding topic from the WebHelp Responsive
 */
var actualLocation = window.location.href;
var newLocation;
var request = new XMLHttpRequest();
if (actualLocation.indexOf('/#')!=-1) {
    newLocation = actualLocation.replace(/\/#/g, "/");
}
if (actualLocation.match(/\/index\.(.*)#/gi)!=null) {
    newLocation = actualLocation.replace(/\/index\.(.*)#/gi, "/");
}
if (typeof newLocation != "undefined") {
    request.open('GET', newLocation, true);
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            if (request.status !== 404) {
                window.location.replace(newLocation);
            }
        }
    };
    request.send();
}