
/* 轮播图初始化 */
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
/* 加 
--------------------------*/
$('.pull-left.grey').on("click", '#addition', function () {
    var quantity = parseInt($('#carnum').val());
    $('#carnum').val(quantity + 1); 
});

/* 减去 
--------------------------*/
$('.pull-left.grey').on("click", '#subtraction', function () {
    var quantity = parseInt($('#carnum').val());
    if(quantity>1){
        $('#carnum').val(quantity - 1); 
    }
});



/* 商品信息存入COOKIE */
function productCookie(){
    var products = new Array();
    var product = {};
        product.name = $('.item_name').text();
        product.rule = $('.rule_name').text();
        product.img = $('#big_img').attr('src');
        product.Price = $('.unit-price').text();
        product.ruleid = $('.rule_tr').attr('ruleid');
        product.num = $('#carnum').text();
        products.push(product);
    products = JSON.stringify(products);
    CookieUtil.set("products", products, '', "/");
    //cookie保存总价
    var sum_price = $('#total_price').text();
    CookieUtil.set("sum_price", sum_price, '', "/");
};



/*加入购物车提交程序封装
--------------------------*/
function ajaxSubmit() {
    var url = '/shopcar/shopcars/';
    var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    var ruleid = $('.act_box').attr('ruleid')
    var quantity = parseInt($('#carnum').text());
    var data = {
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

/*“加入购物车”按钮绑定事件*
--------------------------*/
 $('.add-cart').click(function () {
    getLogin();
    if ($('.act_box').length === 0) {
        $('.rule_wrap').find('.red_msg').remove();
        $('.rule_wrap').append('<p class="red_msg">请选择</p>');
    } else {
        ajaxSubmit();
    }
});




/* 限制价格小数点后面两位数 */
var total_price=$('#total_price').text()-0;
$('#total_price').text(total_price.toFixed(2));
