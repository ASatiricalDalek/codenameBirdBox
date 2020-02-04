$(function() {
    $('a#feed').bind('click', function() {
        $.getJSON($SCRIPT_ROOT + '/_feed')
    })
});
