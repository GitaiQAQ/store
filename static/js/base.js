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

//获得带参数的完整url
function loadQueryString(){ 
    var parameters = {}; 
    var searchString = location.search.substr(1); 
    var pairs = searchString.split("&"); 
    var parts;
    for(i = 0; i < pairs.length; i++){
        parts = pairs[i].split("=");
        var name = parts[0];
        var data = decodeURI(parts[1]);
        parameters[name] = data;
    }
    return parameters;
}

function fnLimited(inputLimited){
    inputLimited.keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
             // Allow: Ctrl+A, Command+A
            (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) || 
             // Allow: home, end, left, right, down, up
            (e.keyCode >= 35 && e.keyCode <= 40)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });
}




function fixedFooter(){//页面过小时，底部固定
    var docHeight=$('body').height();//整个网页的高度
    var windowHeight= $(window).height();//浏览器可视窗口的高度
    if(docHeight<windowHeight){
        $('.linkitems').css({'position':'fixed','bottom':'40px','width':'100%'});
        $('footer').css({'position':'fixed','bottom':'0px','width':'100%'});
    }
}
$(function(){
     /* 
   让复选框CSS插件生效
   */
  $('.magic-checkbox').each(function(){
    var i = $('.magic-checkbox').index($(this));
    $('.magic-checkbox').eq(i).attr('id','c'+i);
    $('.magic-checkbox + label').eq(i).attr('for','c'+i);
});
})