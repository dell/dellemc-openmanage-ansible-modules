define(["options", "jquery", "nav"], function (options, $, navConfig) {

    /**
     * The path of the output directory, relative to the current HTML file.
     * @type {String}
     */
    var path2root = null;

    // Register the hover handler for the Menu
    $(document).ready ( function() {
        // Add mouse listener and set the wai-aria attributes to the new value, depending on the expanded/collapsed state
        $(document).on("mouseenter", ".wh_top_menu li", menuItemHovered);

        // Mouse exit
        $(document).on("mouseleave", ".wh_top_menu li", function () {
            var stateNode = $(this).children(".topicref");
            var currentState = stateNode.attr(navConfig.attrs.state);
            if (currentState !== navConfig.states.leaf) {
                $(this).attr("aria-expanded", "false");
                stateNode.attr(navConfig.attrs.state, navConfig.states.collapsed);
            }
        });
    });

    /**
     * Retrieves the path of the output directory, relative to the current HTML file.
     *
     * @returns {*} the path of the output directory, relative to the current HTML file.
     */
    function getPathToRoot() {
        if (path2root == null) {
            path2root = $('meta[name="wh-path2root"]').attr("content");
            if (path2root == null || path2root == undefined) {
                path2root = "";
            }
        }
        return path2root;
    };

    /**
     * Loads the JS file containing the list of child nodes for the current topic node.
     * Builds the list of child topics element nodes based on the retrieved data.
     *
     * @param topicRefSpan The topicref 'span' element of the current node from TOC / Menu.
     */
    function retrieveChildNodes(topicRefSpan) {
        var tocId = $(topicRefSpan).attr(navConfig.attrs.tocID);
        if (tocId != null) {
            var jsonHref = navConfig.jsonBaseDir + "/" + tocId;
            require(
                [jsonHref],
                function(data) {
                    if (data != null) {
                        var topics = data.topics;
                        var topicLi = topicRefSpan.closest('li');
                        var topicsLiList = createTopicsList(topics);

                        var loadingDotsUl = topicLi.children("ul.loading");
                        // Remove the loading dots from the menu.
                        loadingDotsUl.find('li').remove();
                        loadingDotsUl.removeClass('loading');

                        topicsLiList.forEach(function(topicLi){
                            loadingDotsUl.append(topicLi);
                        });

                        topicRefSpan.attr(navConfig.attrs.state, navConfig.states.expanded);
                    } else {
                        topicRefSpan.attr(navConfig.attrs.state, navConfig.states.leaf);
                    }
                }
            );
        }
    }

    /**
     * Creates the <code>ul</code> element containing the child topic nodes of the current topic.
     *
     * @param topics The array of containing info about the child topics.
     *
     * @returns {*|jQuery|HTMLElement} the <code>li</code> elements representing the child topic nodes of the current topic.
     */
    function createTopicsList(topics) {
        var topicsArray = [];
        topics.forEach(function(topic) {
            if (!topic.menu.isHidden) {
                var topicLi = createTopicLi(topic);
                topicsArray.push(topicLi);
            }
        });
        return topicsArray;
    };

    /**
     * Creates the <code>li</code> element containing a topic node.
     *
     * @param topic The info about the topic node.
     *
     * @returns {*|jQuery|HTMLElement} the <code>li</code> element containing a topic node.
     */
    function createTopicLi(topic) {
        var li = $("<li role=\"menuitem\">");

        if (topic.menu.hasChildren) {
            li.addClass("has-children");
            li.attr("aria-haspopup", "true");
            li.attr("aria-expanded", "false");
        }
        var topicImage = topic.menu.image;
        if (topicImage != null && topicImage.href != null) {
            var menuImageSpan = createMenuImageSpan(topic);
            li.append(menuImageSpan);
        }

        // .topicref span
        var topicRefSpan = createTopicRefSpan(topic);
        // append the topicref node in parent
        li.append(topicRefSpan);

        return li;
    };

    /**
     * Creates the <span> element containing the image icon for the current node in the menu.
     * @param topic The JSON object containing the info about the associated node.
     *
     * @returns {*|jQuery|HTMLElement} the image 'span' element.
     */
    function createMenuImageSpan(topic) {
        var topicImage = topic.menu.image;
        // Image span
        var imgSpan = $("<span>", {class : "topicImg"});

        var isExternalReference = topicImage.scope == 'external';
        var imageHref = '';
        if (!isExternalReference) {
            imageHref += getPathToRoot();
        }
        imageHref += topicImage.href;

        var img = $("<img>", {
            src : imageHref,
            alt : topic.title
        });

        if (topicImage.height != null) {
            img.attr("height", topicImage.height);
        }
        if (topicImage.width != null) {
            img.attr("width", topicImage.width);
        }
        imgSpan.append(img);

        return imgSpan;
    }

    /**
     * Creates the <span> element containing the title and the link to the topic associated to a node in the menu or the TOC.
     *
     * @param topic The JSON object containing the info about the associated node.
     *
     * @returns {*|jQuery|HTMLElement} the topic title 'span' element.
     */
    function createTopicRefSpan(topic) {
        var isExternalReference = topic.scope == 'external';

        // .topicref span
        var topicRefSpan = $("<span>");
        topicRefSpan.addClass("topicref");
        if (topic.outputclass != null) {
            topicRefSpan.addClass(topic.outputclass);
        }

        // WH-1820 Copy the Ditaval "pass through" attributes.
        var dataAttributes = topic.attributes;
        if (typeof dataAttributes !== 'undefined') {
            var attrsNames = Object.keys(dataAttributes);
            attrsNames.forEach(function(attr) {
                topicRefSpan.attr(attr, dataAttributes[attr]);
            });
        }

        topicRefSpan.attr(navConfig.attrs.tocID, topic.tocID);
        topicRefSpan.attr("id", topic.tocID + "-mi");

        // Current node state
        var containsChildren = hasChildren(topic);
        if (containsChildren) {
            // This state means that the child topics should be retrieved later.
            topicRefSpan.attr(navConfig.attrs.state, navConfig.states.notReady);
        } else {
            topicRefSpan.attr(navConfig.attrs.state, navConfig.states.leaf);
        }

        // Topic ref link
        var linkHref = '';
        if (topic.href != null && topic.href != 'javascript:void(0)') {
            if (!isExternalReference) {
                linkHref += getPathToRoot();
            }
            linkHref += topic.href;
        }
        var link = $("<a>", {
            href: linkHref,
            html: topic.title
        });

        // WH-2368 Update the relative links
        var pathToRoot = getPathToRoot();
        var linksInLink = link.find("a[href]");
        linksInLink.each(function () {
            var href = $(this).attr("href");
            if (!(href.startsWith("http:") || href.startsWith("https:"))) {
                $(this).attr("href", pathToRoot + href);
            }
        });
        var imgsInLink = link.find("img[src]");
        imgsInLink.each(function () {
            var src = $(this).attr("src");
            if (!(src.startsWith("http:") || src.startsWith("https:"))) {
                $(this).attr("src", pathToRoot + src);
            }
        });

        if (isExternalReference) {
            link.attr("target", "_blank");
        }
        var titleSpan = $("<span>", {
           class: "title"
        });

        titleSpan.append(link);
        topicRefSpan.append(titleSpan);

        return topicRefSpan;
    }

    function hasChildren(topic) {
        // If the "topics" property is not specified then it means that children should be loaded from the
        // module referenced in the "next" property
        var children = topic.topics;
        var hasChildren;
        if (children != null && children.length == 0) {
            hasChildren = false;
        } else if (topic.menu != null) {
            hasChildren = topic.menu.hasChildren;
        } else {
            hasChildren = true;
        }
        return hasChildren;
    }

    function menuItemHovered() {
        var topicRefSpan = $(this).children('.topicref');
        var state = topicRefSpan.attr(navConfig.attrs.state);
        if (state === navConfig.states.pending) {
            // Do nothing
        } else if (state === navConfig.states.notReady) {
            topicRefSpan.attr(navConfig.attrs.state, navConfig.states.pending);

            var menuItemID = topicRefSpan.attr("id");
            var dot = $("<span>", {
                class: "dot"
            });
            var loadingMarker =
                $("<ul>", {
                    class: "loading",
                    "aria-labelledby" : menuItemID,
                    role : "menu",
                    html: $("<li>", {
                        role : "menuitem",
                        html: [dot, dot.clone(), dot.clone()]
                    })
                });

            $(this).append(loadingMarker);

            handleMenuPosition($(this));
            retrieveChildNodes(topicRefSpan);

        } else if (state === navConfig.states.expanded) {
            handleMenuPosition($(this));
        } else if (state === navConfig.states.collapsed) {
            topicRefSpan.attr(navConfig.attrs.state, navConfig.states.expanded);
        }

        if ($(this).attr("aria-expanded") != null) {
            $(this).attr("aria-expanded", "true");
        }
    };

    var dirAttr = $('html').attr('dir');
    var rtlEnabled = false;
    if (dirAttr=='rtl') {
        rtlEnabled = true;
    }

    /**
     * Display top menu so that it will not exit the viewport.
     *
     * @param $menuItem The top menu menu 'li' element of the current node from TOC / Menu.
     */
    function handleMenuPosition($menuItem) {
        // Handle menu position
        var parentDir = rtlEnabled ? 'left' : 'right';
        var index = $('.wh_top_menu ul').index($menuItem.parent('ul'));

        var currentElementOffsetLeft = parseInt($menuItem.offset().left);
        var currentElementWidth = parseInt($menuItem.width());
        var currentElementOffsetRight = currentElementOffsetLeft + currentElementWidth;
        var nextElementWidth = parseInt($menuItem.children('ul').width());
        var offsetLeft,
            offsetRight = currentElementOffsetRight + nextElementWidth;

        if (index == 0) {
            if (parentDir=='left') {
                $menuItem.attr('data-menuDirection', 'left');
                offsetLeft = currentElementOffsetRight - nextElementWidth;
                if (offsetLeft <= 0) {
                	$menuItem.css('position', 'relative');
	                $menuItem.children('ul').css('position','absolute');
                    $menuItem.children('ul').css('right', 'auto');
                    $menuItem.children('ul').css('left', '0');
                }
            } else {
                $menuItem.attr('data-menuDirection', 'right');
                offsetRight = currentElementOffsetLeft + nextElementWidth;
                if (offsetRight >= $(window).width()) {
                    $menuItem.css('position', 'relative');
                    $menuItem.children('ul').css('position','absolute');
                    $menuItem.children('ul').css('right', '0');
                    $menuItem.children('ul').css('left', 'auto');
            	}
            }
        } else {
            offsetLeft = currentElementOffsetLeft - nextElementWidth;

            if (parentDir == 'left') {
                if (offsetLeft >= 0) {
                    $menuItem.attr('data-menuDirection', 'left');
                    $menuItem.children('ul').css('right', '100%');
                    $menuItem.children('ul').css('left', 'auto');
                } else {
                    $menuItem.attr('data-menuDirection', 'right');
                    $menuItem.children('ul').css('right', 'auto');
                    $menuItem.children('ul').css('left', '100%');
                }
            } else {
                if (offsetRight <= $(window).width()) {
                    $menuItem.attr('data-menuDirection', 'right');
                    $menuItem.children('ul').css('right', 'auto');
                    $menuItem.children('ul').css('left', '100%');
                } else {
                    $menuItem.attr('data-menuDirection', 'left');
                    $menuItem.children('ul').css('right', '100%');
                    $menuItem.children('ul').css('left', 'auto');
                }
            }
        }
    }
});
