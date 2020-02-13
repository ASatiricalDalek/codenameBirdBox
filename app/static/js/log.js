$(function() {
    $('a#log').bind('click', function() {
        $.getJSON($SCRIPT_ROOT + '/_log')
    })
});
