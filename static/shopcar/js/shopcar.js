/* 
 *提示登录
 */
$('document').ready(function () {
    getLogin();
})

/* 
 *checkbox click
 *全选/反选
 */
/*
$("#all_checked").click(function() {
    if (this.checked) {
        $("input.checked").prop("checked", true);
    } else {
        $("input.checked").prop("checked", false);
    }
});
*/
$('#all_checked').on('ifChecked', function () {
    //全选勾选
    $('.ichecked_item').iCheck('check');
});

$('#all_checked').on('ifUnchecked', function () {
    //全选取消勾选
    if ($('#all_checked').attr("remove") == "undefined") {
        // 如果之前全选了，现在其中某个选项不需要选了，这时不需要触发ifUnchecked事件
        $('.ichecked_item').iCheck('uncheck');
    }
});

/* 按钮选中显示总价*/
var selectList = '';
/*
$('body').on("click", "input[type='checkbox']", function() {
    selectList = $("input.checked:checked").parents('.car-list');
    //cal_sum();
    var sum = cal_sum();
    $('.sum_price').text(sum);
    var nub =nub_sum();
    $('.nub-sum').text(nub);
});
 */

function itemcheck() {
    selectList = $("input.checked:checked").parents('.car-list');

    var sum = cal_sum();
    $('.sum_price').text(sum);
    var nub = nub_sum();
    $('.nub-sum').text(nub);
}


$('.ichecked_item').on('ifChecked', function () {
    if ($('.ichecked_item:checked').length == $('.ichecked_item').length) {
        //全部都被选中了
        $('#all_checked').iCheck('check');
    }
    itemcheck();
});

$('.ichecked_item').on('ifUnchecked', function () {
    //$('#all_checked').parents().removeClass("checked");

    $('#all_checked').attr("remove", "1");
    $('#all_checked').iCheck('uncheck');

    //$('#all_checked').parents().removeClass("checked");
    itemcheck();
});




$('.ichecked_item, #all_checked').iCheck({
    checkboxClass: 'icheckbox_flat-red',
    radioClass: 'iradio_flat-red',
    increaseArea: '20%'
});
/* 
 *加载完跟新价格
 */
window.onload = function () {
    var selectList = $("input.checked:checked").parents('.car-list');
    //cal_sum();
    var sum = cal_sum();
    $('.sum_price').text(sum);
    var nub = nub_sum();
    $('.nub-sum').text(nub);
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
/* 总件数 */
function nub_sum() {
    var num = 0;
    var sum = 0; //tatol money
    for (var i = 0; i < selectList.length; i++) {
        price = parseFloat($(selectList[i]).find('.carprice').text());
        num = parseFloat($(selectList[i]).find('.carnum').text());
        sum += num;
    }
    return sum;
};

/* 
 *加按钮
 */
$('.car-list').on("click", '.addition', function () {
    var quantity = $(this).next().text();
    var quantity = parseInt(quantity);
    $(this).next().text(quantity + 1);
    var now_num = $(this).next().text();

    /* 小计 */
    var price = $(this).parents('tr').find('.carprice').text();
    var small_sum = price * now_num;
    $(this).parents('tr').find('.small_sum').text(small_sum);
    /* 总价 */
    var sum = cal_sum();
    $('.sum_price').text(sum);
    /* 总件 */
    var nub = nub_sum();
    $('.nub-sum').text(nub);
});
/* 
 *减按钮
 */
$('.car-list').on("click", '.subtraction', function () {
    var quantity = $(this).prev().text();
    var quantity = parseInt(quantity);
    if (quantity < 1) {
        $(this).prev().text(0);
    } else {
        $(this).prev().text(quantity - 1);
        /* 总价 */
        var sum = cal_sum();
        $('.sum_price').text(sum);
        /* 小计 */
        var now_num = $(this).prev().text();
        var price = $(this).parents('tr').find('.carprice').text();
        var small_sum = price * now_num;
        $(this).parents('tr').find('.small_sum').text(small_sum);
        /* 总件 */
        var nub = nub_sum();
        $('.nub-sum').text(nub);
    };
});

/* 
 *提交按钮
 */
$('a#buy').click(function () {
    if (selectList.length < 1) {
        $().errormessage('未选中商品！');
        return;
    }
    //创建商品列表数组，每个元素是一个商品对象
    var products = new Array();
    for (var i = 0; i < selectList.length; i++) {
        var aName = $(selectList[i]).find('.carlist_name'),
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
        product.rulename = aCarnum.attr('desc');
        product.num = aCarnum.text();
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
$('.car-list').on('click', '.delete', function () {
    var fa_times = $(this);
    data = {
        'method': 'delete',
        'ruleid': fa_times.attr('ruleid'),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    $.ajax({
        type: 'post',
        url: '/shopcar/shopcars/',
        data: data,
        success: function (result) {
            if (result['status'] == 'ok') {
                fa_times.parents('.car-list').remove();
                fixedFooter();//如果网页高度不够底部固定。
                var selectList = $("input.checked:checked").parents('.car-list');
                var sum = cal_sum();
                $('.sum_price').text(sum);
                var nub = nub_sum();
                $('.nub-sum').text(nub);
            }
        },
        error: function () {
            $().errormessage('server is down!');
        }
    })
});
/*
* 全部删除
*/
$('#all-delete').click(function () {
    data = {
        'method': 'delete',
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    if (selectList.length) {
        for (var i = 0; i < selectList.length; i++) {
            var ruleid = $(selectList[i]).find('.carnum').attr('ruleid');
            data['ruleid'] = ruleid;
            $.ajax({
                type: 'post',
                url: '/shopcar/shopcars/',
                data: data,
                success: function (result) {
                    if (result['status'] == 'ok') {
                        fixedFooter();
                        var selectList = $("input.checked:checked").parents('.car-list');
                        var sum = cal_sum();
                        $('.sum_price').text(sum);
                        var nub = nub_sum();
                        $('.nub-sum').text(nub);
                    }
                },
                error: function () {
                    $().errormessage('server is down!');
                }
            })
        }
        location.href = "/shopcar/shopcars/";
    }
    else {
        $().errormessage('请先选择...');
    }
});
