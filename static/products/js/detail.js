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
 * 件数输入框失去焦点事件
 */
$('#carnum').on('blur',function(){
    total();
});

/* 
 * ‘型号’点击事件
 */
$('.edition').on('click',function(){
    if( $(this).hasClass('active-rule')){
        $(this).removeClass('active-rule');
        $('#total_price').text('0');
    }else{
        $('.edition').removeClass('active-rule');
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

/* 
 * 个数输入--禁止输入除数字之外的其他字符和0
 */
$("#carnum").keyup(function(){    
    $(this).val($(this).val().replace(/[^1-9.]/g,''));    
}).bind("paste",function(){  //CTR+V事件处理    
    $(this).val($(this).val().replace(/[^1-9.]/g,''));     
}).css("ime-mode", "disabled"); //CSS设置输入法不可用





/* 
 * “加入购物车”按钮绑定事件
 */
$('#add-cart').click(function () {
    getLogin();
    if ($('.act_box').length === 0) {
        $('.rule_wrap').find('.red_msg').remove();
        $('.rule_wrap').append('<p class="red_msg">请选择</p>');
    } else {
        ajaxSubmit();
    }
});

/* 
 * 封装‘ajax提交’函数
 */
function ajaxSubmit() {
    var url = '/product/products/',
        csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val(),
        ruleid = $('.act_box').attr('ruleid'),
        quantity = parseInt($('#carnum').text()),
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
