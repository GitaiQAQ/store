$(document).ready(function(){
    /* for(var i=0;i<$('.item').length;i++){
        var number =$('.price-sum').eq(i).parents('.item').find('.nub').text(),
            price = $('.price-sum').eq(i).parents('.item').find('.price').text(),
            sum = number*price
        $('.price-sum').eq(i).text(sum);
    } */
    $(".price-sum").each(function(){
        var number =$(this).parents('.item').find('.nub').text(),
            price = $(this).parents('.item').find('.price').text(),
            sum = number*price
            $(this).text(sum);
      });
})