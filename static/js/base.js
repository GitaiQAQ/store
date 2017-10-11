function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
/* 
 *返回按钮
 */
$(document).ready(function() {
    $('i.back').click(function() {
        history.back();
    });
});
/* 
 *菜单栏搜索框
 */
$('input.search').focus(function() {
    $('#search-form').css('border-bottom', '1px solid #44a8f2');
});
$('input.search').blur(function() {
    $('#search-form').css('border-bottom', '0px');
});