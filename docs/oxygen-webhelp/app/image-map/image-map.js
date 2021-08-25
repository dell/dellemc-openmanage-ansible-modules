define(["require", "jquery"], function (require, $) {
    $(document).ready(function () {
        // If we have image maps in our HTML document then we should load the highlight and resize libraries.
        var imageMaps = $('img[usemap]');

        if (imageMaps.length > 0) {
            require(["jquery.maphilight", "jquery.rwdImageMaps"], function () {
                /**
                 * Responsive highlighted image maps
                 */
                $('img[usemap]').rwdImageMaps();
                $('img[usemap]').maphilight();
            });
        }
    });
});