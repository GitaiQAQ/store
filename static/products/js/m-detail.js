/* 
 * 轮播图初始化 
 */

$(document).ready(function(){
    var swiper = new Swiper('.swiper-container', {
       pagination: '.swiper-pagination',
       paginationClickable: true,
       // Enable debugger
       debugger: true,
       autoplay : 5000,
       loop : true
   });
})

//初始化：页面加载的时候默认现则第一个规格
if ($(".edition").length > 0){
     $(".edition:first").addClass("active-rule");
     $("#total_price").text($(".edition:first").attr("data-price"));
     $("#inventory").text($(".edition:first").attr("inventory"));
}
if ($(".b_color").length > 0){
    $(".b_color:first").addClass("active-color");
}

/* 
 * 增加产品个数
 */
$('.pull-left.grey').on("click", '#addition', function () {
    var quantity = parseInt($('#carnum').val());
    var detection= parseInt($('#inventory').text());
    if(!isNaN(detection)){//如果库存是数字
        if(quantity<detection){
            $('#carnum').val(quantity + 1);
        }
    }else{//如果库存是有货
        if(quantity<300){//有货且输入小于300
            $('#carnum').val(quantity + 1);
        }else{//有货且输入大于300
            $("#carnum").val(300);
            $().message('最多可选择300件！');
        }
    }
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
        //$(this).removeClass('active-rule');
        //$('#total_price').text('0');
    }else{
        $(this).siblings('.edition').removeClass('active-rule');
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
        inventory = $('.active-rule').attr('inventory'),
        totalPrice = nub*price;
    if($('.active-rule').length>0){
        $('#total_price').text(totalPrice);
        $('#inventory').text(inventory);
        if (inventory == '0'){
            $("#add-cart").attr('disabled', 'disabled');
            $("#add-cart").removeClass('orange-bg');
            $("#add-cart").addClass('grey-bg');
            $("#add-cart").text('已售罄');
        }
        else{
            $("#add-cart").removeAttr('disabled');
            $("#add-cart").addClass('orange-bg');
            $("#add-cart").removeClass('grey-bg');
            $("#add-cart").text('加入购物车');
        }
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
$("#carnum").on('keyup change',function () {
    var detection = parseInt($('#inventory').text());
    if (!isNaN(detection)) {//如果库存是数字
        if ($("#carnum").val() > detection) {//个数选到最大库存后不再增长
            $("#carnum").val(detection);
        } else {
            $(this).val($(this).val().replace(/[^\d]/g, ''));
        }
    } else if($(this).val()>300){
        $("#carnum").val(300);
        $().message('最多可选择300件！');
    }
}).bind("paste", function () {  //CTR+V事件处理
    $(this).val($(this).val().replace(/[^0-9]/g, ''));
}).css("ime-mode", "disabled"); //CSS设置输入法不可用

/* 
 * 件数输入框焦点事件
 */
$('#carnum').on('focus',function(){
    $('.msg').remove();
});
$('#carnum').on('blur',function(){
    var detection= parseInt($('#inventory').text());
    
    if($('#carnum').val()==''||$('#carnum').val()==0){
       $('.msg').remove();
       $(this).val(1);
       total();
      /*  $(this).parent().after('<span class="msg orange fs12">数量不能为空!</span>') */
    }
});
/* 
 * “加入购物车”按钮绑定事件
 */
$('#add-cart').click(function () {
    getLogin();
    if ($('.active-rule').length == 0) {
        $('.rulemsg').remove();
        $('.edition').parent().append('<span class="rulemsg orange fs12">规格未选择!</span>');
    } else if (!$('.b_color').attr('data-color') == ''&&$('.active-color').length == 0) {
            $('.colormsg').remove();
            $('.b_color').parent().append('<span class="colormsg orange fs12">表带颜色未选择!</span>');
    } else if ($('#carnum').val() == '') {
        return;
    }
    else {
        ajaxSubmit();
    }
});
$('#bye-now').click(function () {
    getLogin();
    if ($('.active-rule').length == 0) {
        $('.rulemsg').remove();
        $('.edition').parent().append('<span class="rulemsg orange fs12">规格未选择!</span>');
    } else if (!$('.b_color').attr('data-color') == ''&&$('.active-color').length == 0) {
            $('.colormsg').remove();
            $('.b_color').parent().append('<span class="colormsg orange fs12">表带颜色未选择!</span>');
    } else if ($('#carnum').val() == '') {
        return;
    }
    else {
        ajaxByeNow();
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
        title =  $('.item_name').text(),
        desc=$('.active-rule').text();
        if ($('.active-color').attr("data-color-title") != undefined){
            desc += $('.active-color').attr("data-color-title");
        }
        data = {
        'method': 'create',
        'ruleid': ruleid,
        'num': quantity,
        'desc':desc,
        'title':title,
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
        }
    });
}
/* 立即购买ajax */
function ajaxByeNow() {
    //创建商品列表数组，每个元素是一个商品对象
    var products = new Array();
    product = {};
        product.name = $('.item_name').text();//ok
        product.rule =$('.active-rule').text()+$('.active-color').attr('data-color-title'); 
        product.img = $('.item_name').attr('data-img-url'); 
        product.Price = $('.active-rule').attr('data-price');//ok
        product.ruleid = $('.active-rule').attr('ruleid');//ok
        product.rulename = $('.active-rule').text()+$('.active-color').attr('data-color-title'); 
        product.num = $('#carnum').val();
        products.push(product);
    //商品列表数组保存到cookie
    products = JSON.stringify(products);
    CookieUtil.set("products", products, '', "/");
    //cookie保存总价
    var sum_price = $('#total_price').text();
    CookieUtil.set("sum_price", sum_price, '', "/");
    window.location.href = '/bill/bills/?new';
}


/* 下拉置顶加入购物车 */

$(function(){  
    //获取导航距离页面顶部的距离  
    var toTopHeight =$('.add-cart-wrap').offset().top;  
      
    //监听页面滚动  
    $(window).scroll(function() {  
        //判断页面滚动超过导航时执行的代码  
        if( $(document).scrollTop() > toTopHeight ){  
            //检测是否为IE6。jQuery1.9中去掉了msie的方法，所以只好这样写  
            if ('undefined' == typeof(document.body.style.maxHeight)) {  
                //页面滚动的距离  
                var scrollTop = $(document).scrollTop();  
                //IE6下，用absolute定位，并设置Top值为距离页面顶部的距离  
               $('.add-cart-wrap').css({'position':'absolute','top':scrollTop+'px'});  
            }else{  
                //IE6以上浏览器采用fixed定位  
               $('.add-cart-wrap').addClass("nav_fixed");  
            }  
        }else{//判断页面滚动没有超过导航时执行的代码  
            if ('undefined' == typeof(document.body.style.maxHeight)) {  
                //设置Top值为导航距页面顶部的初始值。（IE6为了防止浏览器一下滚动过多，所以不能采用直接去掉定位的方法）  
               $('.add-cart-wrap').css({'position':'absolute','top':toTopHeight+'px'});  
            }else{  
                //IE6以上浏览器移除fixed定位，采用默认流布局  
               $('.add-cart-wrap').removeClass("nav_fixed");  
            }  
        }  
    });  
});