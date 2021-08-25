define(["options", "jquery", "nav"], function (options, $, navConfig) {

    /**
     * The path of the output directory, relative to the current HTML file.
     * @type {String}
     */
    var path2root = null;

    $(document).ready(function () {
        // Register the click handler for the TOC
        var topicRefExpandBtn = $(".wh_publication_toc .wh-expand-btn");
        topicRefExpandBtn.click(toggleTocExpand);

        /* Toggle expand/collapse on enter and space */
        topicRefExpandBtn.keypress(handleKeyEvent);
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

    /* 
     * Toggles expand/collapse on enter and space 
     */
    function handleKeyEvent(event) {
        // Enter & Spacebar events
        if (event.which === 13 || event.which === 32) {
            event.preventDefault();
            toggleTocExpand.call(this);
        }
    }

    function toggleTocExpand() {

        var topicRef = $(this).closest(".topicref");
        var state = topicRef.attr(navConfig.attrs.state);
        var parentLi = $(this).closest('li');
        var titleLink = $(this).siblings(".title").children("a");
        var titleLinkID = titleLink.attr("id");

        if (state == null) {
            // Do nothing
        } else if (state == navConfig.states.pending) {
            // Do nothing
        } else if (state == navConfig.states.notReady) {
            topicRef.attr(navConfig.attrs.state, navConfig.states.pending);
            parentLi.attr('aria-expanded', 'true');
            $(this).attr("aria-labelledby", navConfig.btnIds.pending + " " + titleLinkID);
            retrieveChildNodes(topicRef);
        } else if (state == navConfig.states.expanded) {
            topicRef.attr(navConfig.attrs.state, navConfig.states.collapsed);
            $(this).attr("aria-labelledby", navConfig.btnIds.expand + " " + titleLinkID);
            parentLi.attr('aria-expanded', 'false');
        } else if (state == navConfig.states.collapsed) {
            topicRef.attr(navConfig.attrs.state, navConfig.states.expanded);
            $(this).attr("aria-labelledby", navConfig.btnIds.collapse + " " + titleLinkID);
            parentLi.attr('aria-expanded', 'true');
        }
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
                function (data) {
                    if (data != null) {
                        var topics = data.topics;
                        var topicLi = topicRefSpan.closest('li');
                        var topicsUl = createTopicsList(topics);

                        var topicsUlParent = $('<ul role="group"/>');
                        topicsUl.forEach(function (topic) {
                            topicsUlParent.append(topic);
                        });
                        topicLi.append(topicsUlParent);

                        var titleLink = topicRefSpan.find(".title > a");
                        var titleLinkID = titleLink.attr("id");

                        var expandBtn = topicRefSpan.children('.wh-expand-btn');
                        expandBtn.attr("aria-labelledby", navConfig.btnIds.collapse + " " + titleLinkID);

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
        topics.forEach(function (topic) {
            var topicLi = createTopicLi(topic);
            topicsArray.push(topicLi);
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
        var li = $("<li>");
        li.attr('role', 'treeitem');
        if (hasChildren(topic)) {
            li.attr('aria-expanded', 'false');
        }

        // .topicref span
        var topicRefSpan = createTopicRefSpan(topic);
        // append the topicref node in parent
        li.append(topicRefSpan);

        return li;
    };

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
            attrsNames.forEach(function (attr) {
                topicRefSpan.attr(attr, dataAttributes[attr]);
            });
        }

        topicRefSpan.attr(navConfig.attrs.tocID, topic.tocID);

        // Current node state
        var menuHasChildren = topic.menu.hasChildren;
        var containsChildren = hasChildren(topic);
        if (containsChildren && menuHasChildren) {
            // This state means that the child topics should be retrieved later.
            topicRefSpan.attr(navConfig.attrs.state, navConfig.states.notReady);
        } else {
            topicRefSpan.attr(navConfig.attrs.state, navConfig.states.leaf);
        }

        var expandBtn = $("<span>", {
            class: "wh-expand-btn",
            role: "button"
        });

        if (containsChildren) {
            expandBtn.attr("aria-labelledby", navConfig.btnIds.expand + " " + getTopicLinkID(topic));
            expandBtn.attr("tabindex", "0");
        }

        expandBtn.click(toggleTocExpand);
        expandBtn.keypress(handleKeyEvent);
        topicRefSpan.append(expandBtn);

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

        link.attr("id", getTopicLinkID(topic));

        if (isExternalReference) {
            link.attr("target", "_blank");
        }
        var titleSpan = $("<span>", {
            class: "title"
        });

        titleSpan.append(link);

        // Topic ref short description
        if (topic.shortdesc != null) {
            var tooltipSpan = $("<span>", {
                class: "wh-tooltip",
                html: topic.shortdesc
            });

            /* WH-1518: Check if the tooltip has content. */
            if (tooltipSpan.find('.shortdesc:empty').length == 0) {
                // Update the relative links
                var links = tooltipSpan.find("a[href]");
                links.each(function () {
                    var href = $(this).attr("href");
                    if (!(href.startsWith("http:") || href.startsWith("https:"))) {
                        $(this).attr("href", pathToRoot + href);
                    }
                });
                var imgs = tooltipSpan.find("img[src]");
                imgs.each(function () {
                    var src = $(this).attr("src");
                    if (!(src.startsWith("http:") || src.startsWith("https:"))) {
                        $(this).attr("src", pathToRoot + src);
                    }
                });

                titleSpan.append(tooltipSpan);
            }
        }

        topicRefSpan.append(titleSpan);

        return topicRefSpan;
    }

    function getTopicLinkID(topic) {
        return topic.tocID + "-link";
    }

    function hasChildren(topic) {
        // If the "topics" property is not specified then it means that children should be loaded from the
        // module referenced in the "next" property
        var children = topic.topics;
        var hasChildren;
        if (children != null && children.length == 0) {
            hasChildren = false;
        } else {
            hasChildren = true;
        }
        return hasChildren;
    }
});
