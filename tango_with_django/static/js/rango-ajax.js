/**
 * Created with PyCharm.
 * User: user
 * Date: 15.04.14
 * Time: 19:28
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function() {


});

$('#likes').click(function(){
    var catid;
    catid=$(this).attr('data-catid');
    $.get('/rango/like_category/', {category_id: catid}, function(data){
        $('#like_count').html(data);
        $('#likes').hide();
    });
});

function get_data(data){
    $('#cats').html(data);
};

$('#suggestion').keyup(function(){
    var query;
    query=$(this).val();
    $.get('/rango/suggest_category/', {suggestion: query}, get_data);
});

$('.rango-add').click(function(){
    var catid = $(this).attr('data-catid');
    var title = $(this).attr('data-title');
    var url = $(this).attr('data-link');
    var me = $(this);
    $.get('/rango/auto_add_page/', {'category_id': catid, 'title': title, 'url': url}, function(data){
        $('pages').html(data);
        me.hide();
    });
});