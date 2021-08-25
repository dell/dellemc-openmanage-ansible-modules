define(["options", "localization", "jquery"], function (options, i18n, $) {


    var selectors = {
        "expand_buttons": [
            "table.show_hide > caption",
            "table.show_hide_expanded > caption",

            ".fig.show_hide > .figcap",
            ".fig.show_hide_expanded > .figcap",

            "div.show_hide > div.no_title_expander",
            "div.show_hide_expanded > div.no_title_expander",

            ".show_hide_expanded > .sectiontitle:not(.tasklabel)",
            ".show_hide > .sectiontitle:not(.tasklabel)",

            ".task_steps_wraper.show_hide_expanded > .tasklabel",
            ".task_steps_wraper.show_hide > .tasklabel",

            ".example.show_hide_expanded > .tasklabel",
            ".example.show_hide > .tasklabel"
        ]};

    var expandInitialState = options.get("webhelp.topic.collapsible.elements.initial.state");

    /**
     * Add expand-collapse support.
     */
    $(document).ready(function () {
        /* Add the expand/collapse buttons. */
        selectors.expand_buttons.forEach(
            function (selector) {
                var matchedNodes = $(document).find(selector);
                // Add the expand/collapse support only if the title node has visible siblings.
                var visibleSiblings = matchedNodes.siblings(':not(:hidden)');
                if (visibleSiblings.length > 0) {
                    // Add the element with expand/collapse capabilities
                    matchedNodes.append(
                        $("<span>", {
                            "class": "wh_expand_btn expanded",
                            "role": "button",
                            "aria-expanded" : "true",
                            "tabindex" : 0,
                            "aria-label" : i18n.getLocalization("collapse")
                        })
                    );
                    markHiddenSiblingsAsNotExpandable(matchedNodes);
                }
            }
        );

        /*
         * WH-1613
         * Add the permalink icons
         */
        if(selectors.permalinks == 'undefined' || null == selectors.permalinks){
			 console.log("permalinks is undefined");
		 } else {
			selectors.permalinks.forEach(
				function (selector) {
					var matchedNodes = $(document).find(selector);
					// Add the element for the permalink action
					matchedNodes.append("<span class='permalink'/>");
				}
			);
		 }


        /*
         * Slide down when click on a letter from the indexterms bar
         * */
        $('.wh-letters a').click(function (e) {
            var id = $(this).attr('href').replace("#", "");
            e.preventDefault();
            history.replaceState({}, '', e.target.href);

            if ($("[id='" + id + "']").length > 0) {
                $('html, body').animate({scrollTop: $("[id='" + id + "']").offset().top}, 1000);
            }
        });


        /*
         * WH-1613
         * Permalink action
         * */
        $('span.permalink').click(function (e) {
            var id = $(this).closest('[id]').attr('id');
            var hash = '#' + id;
            e.preventDefault();
            history.replaceState({}, '', hash);

            $('html, body').animate({scrollTop: $("[id='" + id + "']").offset().top}, 1000);
        });

        /* Expand / collapse subtopic sections */
        function toggleSubtopics(state) {
            var siblings = $(this).parent().siblings(':not(.wh_not_expandable)');

            if (state !== undefined) {
                // Will expand-collapse the siblings of the parent node, excepting the ones that were marked otherwise
                if (state == 'collapsed') {
                    siblings.slideUp(0);
                    $('.webhelp_expand_collapse_sections').attr('data-next-state', 'expanded').attr('title', i18n.getLocalization('expandSections'));
                    $(this).removeClass('expanded');
                    $(this).attr('aria-expanded', false);
                    $(this).attr('aria-label', i18n.getLocalization('expand'));
                } else {
                    siblings.slideDown(0);
                    $('.webhelp_expand_collapse_sections').attr('data-next-state', 'collapsed').attr('title', i18n.getLocalization('collapseSections'));
                    $(this).addClass('expanded');
                    $(this).attr('aria-expanded', true);
                    $(this).attr('aria-label', i18n.getLocalization("collapse"));
                }
            } else {
                // Change the button state
                $(this).toggleClass("expanded");
                var isExpanded = $(this).hasClass("expanded");
                $(this).attr('aria-expanded', isExpanded);

                if (isExpanded) {
                    $(this).attr('aria-label', i18n.getLocalization("collapse"));
                } else {
                    $(this).attr('aria-label', i18n.getLocalization('expand'));
                }

                var parent = $(this).parent();
                var tagName = parent.prop("tagName");
                // Will expand-collapse the siblings of the parent node, excepting the ones that were marked otherwise
                if (tagName == "CAPTION" || parent.hasClass('wh_first_letter')) {
                    // The table does not have display:block, so it will not slide.
                    // In this case we'll just hide it
                    siblings.toggle();
                } else {
                    siblings.slideToggle("1000");
                }
            }
        }


        /*
         * WH-235
         * Sets the initial state of collapsible elements
         */
        $.each($(document).find('.show_hide_expanded .wh_expand_btn'), function () {
            toggleSubtopics.call(this, "expanded");
        });

        $.each($(document).find('.show_hide .wh_expand_btn'), function () {
            toggleSubtopics.call(this, "collapsed");
        });


        /*
         * Toggle the subtopic sections
         */
        $('.webhelp_expand_collapse_sections').click(function () {
            var state = $('.webhelp_expand_collapse_sections').attr('data-next-state');

            $.each($(document).find('.wh_expand_btn'), function () {
                toggleSubtopics.call(this, state);
            });

            return false;
        });


        /*
         * WH-1750 - Handle topic TOC expand/collapse actions
         */
        $('.wh_topic_toc a').click(function () {
            var currentNode = $(this).attr("href");
            var contentNode = $(currentNode);
            if(contentNode.length){
                $.each(contentNode.parents(), function () {
                    if ($(this).children(".title").length) {
                        toggleSubtopics.call($(this).children('.title').find('.wh_expand_btn'),'expanded');
                    }
                });
                toggleSubtopics.call(contentNode.children('.title').find('.wh_expand_btn'),'expanded');
            }
        });


        /* Expand / collapse support for the marked content */
        var expandWidgets = $(document).find('.wh_expand_btn');
        expandWidgets.click(function (event) {
            toggleSubtopics.call(this);

            return false;
        });

        /* Toggle expand/collapse on enter and space */
        expandWidgets.keypress(function( event ) {
            // Enter & Spacebar events
            if ( event.which === 13 || event.which === 32) {
                event.preventDefault();
                toggleSubtopics.call(this);
            }
        });

    });

    /**
     * Marks the hidden siblings of the matched nodes as being not expandable.
     *
     * @param nodes The matched nodes.
     */
    function markHiddenSiblingsAsNotExpandable(nodes) {
        var siblings = nodes.siblings(":hidden");
        siblings.addClass("wh_not_expandable");
    }
});