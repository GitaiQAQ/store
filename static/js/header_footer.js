
/* 
 *菜单下边线的样式
 */
function menuLine() {
    if ($('.point').length > 1) {
        var leftValue = $('.point:first').offset().left,
            width = $('body').width() - leftValue,
        topValue = $('.point:first').offset().top;
        $('.bottom-line').css('width', width + 'px').css('top', topValue + 2 + 'px');
        /* $('.bottom-line').animate({left:leftValue+'px'},600); */
        $('.bottom-line').css('left', leftValue + 'px');
    }
}
$(window).load(function () {
    menuLine();
})
$(window).resize(function () {
    menuLine();
});
/* -----------------------------------------------------------------------------
 *菜单hover样式
 */
$('.menu-list td').hover(function(){
    $(this).find('.point').addClass('orange-point');
},function(){
    $(this).find('.point').removeClass('orange-point');
})
/* 点击显示qq群二维码 */
$('#qq_group').on('click',function(){
    $('.code-wrap').eq(0).fadeIn(300);
})
$('#wei_group').on('click',function(){
    $('.code-wrap').eq(1).fadeIn(300);
})
$('.close_code').on('click',function(){
    $(this).parents('.code-wrap').fadeOut(300);
})
$('.code-bg').on('click',function(){
    $(this).parents('.code-wrap').fadeOut(300);
})
