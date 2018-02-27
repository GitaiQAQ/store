/* 
 *提示登录
 */
/* $('document').ready(function() {
    getLogin();
}) */

/* 
 *checkbox click
 *全选/反选
 */
$("#all_checked").click(function() {
    if (this.checked) {
        $("input.checked").prop("checked", true);
    } else {
        $("input.checked").prop("checked", false);
    }
});
    /* 按钮选中显示总价*/
var selectList = '';
$('body').on("click", "input[type='checkbox']", function() {
    selectList = $("input.checked:checked").parents('.car-list');
    cal_sum();
    var sum = cal_sum();
    $('.sum_price').text(sum);
});



/* 
 *加载完跟新价格
 */
window.onload = function() {
        var selectList = $("input.checked:checked").parents('.car-list');
        cal_sum();
        var sum = cal_sum();
        $('.sum_price').text(sum);
    }
/* 
 *计算总计价格
 */    
function cal_sum() {
    var num = 0;
    var sum = 0; //tatol money
    for (var i = 0; i < selectList.length; i++) {
        price = parseFloat($(selectList[i]).find('.carprice').text());
        num = parseFloat($(selectList[i]).find('.carnum').text());
        sum += price * num;
    }
    return sum;
};

/* 
 *加按钮
 */
$('.car-list').on("click", '.addition', function() {
    var quantity = $(this).next().text();
    var quantity = parseInt(quantity);
    $(this).next().text(quantity + 1);
    var now_num=$(this).next().text();
    
    /* 小计 */
    var price=$(this).parents('tr').find('.carprice').text();
    var small_sum= price*now_num;
    $(this).parents('tr').find('.small_sum').text(small_sum);
    /* 总价 */
    var sum = cal_sum();
    $('.sum_price').text(sum);
});
/* 
 *减按钮
 */
$('.car-list').on("click", '.subtraction', function() {
    var quantity = $(this).prev().text();
    var quantity = parseInt(quantity);
    if (quantity <1) {
        $(this).prev().text(0);
    } else {
        $(this).prev().text(quantity - 1);
        /* 总价 */
        var sum = cal_sum();
        $('.sum_price').text(sum);
         /* 小计 */
        var now_num=$(this).prev().text();
        var price=$(this).parents('tr').find('.carprice').text();
        var small_sum=price*now_num;
        $(this).parents('tr').find('.small_sum').text(small_sum);
    };
});

/* 
 *提交按钮
 */
$('a.menu-right').click(function() {
    if(selectList.length<1){
        $('.menu-right').css({'background-color':'#505050','color':'#eee'});
        $('.menu-right::after').css({'border-color':'#505050!important'})
        return;
    }
    //创建商品列表数组，每个元素是一个商品对象
    var products = new Array();
    for (var i = 0; i < selectList.length; i++) {
        var aName = $(selectList[i]).find('.car-list_name'),
            aRule = $(selectList[i]).find('.rule_content'),
            aImg = $(selectList[i]).find('img'),
            aPrice = $(selectList[i]).find('.carprice'),
            aCarnum = $(selectList[i]).find('.carnum'),
            product = {};
        product.name = aName.text();
        product.rule = aRule.text();
        product.img = aImg.attr('src');
        product.Price = aPrice.text();
        product.ruleid = aCarnum.attr('ruleid');
        product.num = aCarnum.val();
        products.push(product);
    }
    //商品列表数组保存到cookie
    products = JSON.stringify(products);
    CookieUtil.set("products", products, '', "/");
    //cookie保存总价
    var sum_price = $('.sum_price').text();
    CookieUtil.set("sum_price", sum_price, '', "/");
    window.location.href = '/bill/bills/?new';
})


/* 
 *删除按钮
 */
$('.car-list').on('click','.fa-times',function(){
    var fa_times=$(this);
    data = {
        'method': 'delete',
        'ruleid': $(this).attr('ruleid'),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    $.ajax({
        type: 'post',
        url: '/shopcar/shopcars/',
        data: data,
        success: function(result) {
            if (result['status'] == 'ok'){
                fa_times.parents('.car-list').remove();
            }
            
        },
        error: function(){
          /*   alert('server is down!'); */
        }
    })
});
