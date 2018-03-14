/* 
 *菜单下边线的样式
 */
$(window).load(function () {

    var leftValue = $('.point:first').offset().left,
        width = $('body').width()-leftValue;
    topValue = $('.point:first').offset().top;
    $('.bottom-line').css('width',width+ 'px').css('left', leftValue + 'px').css('top', topValue + 2 + 'px');
})
$(window).resize(function() {
    var leftValue =$('.point:first').offset().left;
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