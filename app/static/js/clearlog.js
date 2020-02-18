$(function() {
    $('a#clear').bind('click', function() {
        $.getJSON($SCRIPT_ROOT + '/_clearfeed')
    })
});