/* 
 *菜单下边线的样式
 */
$(window).load(function () {

    var leftValue = $('.point:first').offset().left,
        width = $('body').width()-leftValue;
    topValue = $('.point:first').offset().top;
    $('.bottom-line').css('width',width+ 'px').css('top', topValue + 2 + 'px');
    /* $('.bottom-line').animate({left:leftValue+'px'},600); */
    $('.bottom-line').css('left',leftValue+'px');
})
$(window).resize(function() {
    var leftValue =$('.point:first').offset().left,
    width = $('body').width()-leftValue;
    $('.bottom-line').css('width',width+ 'px');
    $('.bottom-line').css('left',leftValue+'px');
});
/* -----------------------------------------------------------------------------
 *菜单hover样式
 */
$('.menu-list td').hover(function(){
    $(this).find('.point').addClass('orange-point');
},function(){
    $(this).find('.point').removeClass('orange-point');
})