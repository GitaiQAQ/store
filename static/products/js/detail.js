/* 
 * 轮播图初始化 
 */
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
});

/* 
 * 增加产品个数
 */
$('.pull-left.grey').on("click", '#addition', function () {
    var quantity = parseInt($('#carnum').val());
    $('#carnum').val(quantity + 1); 
    total();
});

/* 
 * 减少产品个数
 */
$('.pull-left.grey').on("click", '#subtraction', function () {
    var quantity = parseInt($('#carnum').val());
    if(quantity>1){
        $('#carnum').val(quantity - 1); 
    };
    total();
});


/* 
 * ‘型号’点击事件
 */
$('.edition').on('click',function(){
    $('.rulemsg').remove();
    if( $(this).hasClass('active-rule')){
        $(this).removeClass('active-rule');
        $('#total_price').text('0');
    }else{
        $(this).siblings('edition').removeClass('active-rule');
        $(this).addClass('active-rule');
        total(); 
    };
});

/* 
 * 商品总价
 */
function total(){
    var nub = $('#carnum').val(),
        price = $('.active-rule').attr('data-price'),
        totalPrice = nub*price;
    if($('.active-rule').length>0){
        $('#total_price').text(totalPrice);
    }else{
        $('#total_price').text('0');
    };
};

/* 
 * 表带颜色
 */
$(document).ready(function(){
    var color = $('.b_color').attr('data-color');
    $('.b_color').css('background-color',color);
});
//选择颜色
$('.b_color').on('click',function(){
    $('.colormsg').remove();
    if( $(this).hasClass('active-color')){
        $(this).removeClass('active-color');
    }else{
        $(this).siblings('b_color').removeClass('active-color');
        $(this).addClass('active-color');
    };
});

/* 
 * 个数输入--禁止输入除数字之外的其他字符和0
 */
$("#carnum").keyup(function(){    
    $(this).val($(this).val().replace(/[^1-9.]/g,''));    
}).bind("paste",function(){  //CTR+V事件处理    
    $(this).val($(this).val().replace(/[^1-9.]/g,''));     
}).css("ime-mode", "disabled"); //CSS设置输入法不可用

/* 
 * 件数输入框焦点事件
 */
$('#carnum').on('focus',function(){
    $('.msg').remove();
});
$('#carnum').on('blur',function(){
    if($('#carnum').val()==''){
       $('.msg').remove();
       $(this).parent().after('<span class="msg orange fs12">数量不能为空!</span>')
    }else{
        total();
    }
});
/* 
 * “加入购物车”按钮绑定事件
 */
$('#add-cart').click(function () {
    getLogin();
    if ($('.active-rule').length === 0) {
        $('.rulemsg').remove();
        $('.edition').parent().append('<span class="rulemsg orange fs12">规格未选择!</span>');
    } else if($('.active-color').length === 0){
        $('.colormsg').remove();
        $('.b_color').parent().append('<span class="colormsg orange fs12">表带颜色未选择!</span>');
    }else if($('#carnum').val()==''){
        return;
    }
     else {
        ajaxSubmit();
    }
});

/* 
 * 封装‘ajax提交’函数
 */
function ajaxSubmit() {
    var url = '/shopcar/shopcars/',
        csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val(),
        ruleid = $('.edition.active-rule').attr('ruleid'),
        quantity =$('#carnum').val(),
        data = {
        'method': 'create',
        'ruleid': ruleid,
        'num': quantity,
        'csrfmiddlewaretoken': csrfmiddlewaretoken
        }

    $.ajax({
        url: url,
        type: 'post',
        data: data,
        success: function (result) {
            if (result['status'] == 'ok') {
                $().message(result['msg']);
            }
            else {
                $().message(result['msg']);
            }
        },
        error: function () { // 500
            $().errormessage('server is down!');
        }
    });
}
