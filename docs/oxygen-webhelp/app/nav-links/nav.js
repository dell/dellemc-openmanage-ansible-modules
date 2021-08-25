define([], function(){

    return {

        attrs : {
            /* The state attribute name */
            state : "data-state",
            id : "data-id",
            tocID : "data-tocid"
        },

        states : {
            /* The possible states */
            pending : "pending",
            notReady : "not-ready",
            collapsed : "collapsed",
            expanded : "expanded",
            leaf : "leaf"
        },

        btnIds : {
            expand : "button-expand-action",
            collapse : "button-collapse-action",
            pending : "button-pending-action"
        },

        jsonBaseDir : "nav-links/json"
    };

});