$(document).ready(function(){
    var swiper = new Swiper('.swiper-container', {
       pagination: '.swiper-pagination',
       paginationClickable: true,
       nextButton: '.swiper-button-next',
       prevButton: '.swiper-button-prev',
       // Enable debugger
       debugger: true,
       autoplay : 5000,
       loop : true
   });
   var positionValue = $('.logo').offset().left;
    $('.shop-link1').css('left',  positionValue +60+ 'px');
    $('.shop-link0').css('right',  positionValue +60+ 'px');
})
$(window).load(function(){
    /* 轮播图箭头位置 */
   var abslut = $('.logo').offset().left;
   $('.swiper-button-prev').css('left', abslut+'px');
   $('.swiper-button-next').css('right', abslut+'px');
   $('.shop-link3').css('left', abslut+60+'px');
})
