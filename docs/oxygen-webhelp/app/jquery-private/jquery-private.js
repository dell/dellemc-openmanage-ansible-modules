/**
 * MAPPING MODULES TO USE NOCONFLICT
 *
 * @see http://requirejs.org/docs/jquery.html#noconflictmap
 */
define(['jquery'], function (jq) {
    return jq.noConflict( true );
});