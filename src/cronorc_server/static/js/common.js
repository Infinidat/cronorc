$(function() {

    // In clickable tables, make the whole row clickable
    $('.table-clickable tbody').on('click', function(event) {
        if (event.target.tagName != 'A') {
            var tr = $(event.target).closest('tr');
            window.location.href = tr.find('a').attr('href');
        }
    });

});
