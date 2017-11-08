/* 
 * 缩略图展示
 */

    var x =$('a.thumbnail_custom img').first().attr('src');
    $('#big_img').attr('src',x);

$('#big_img').height($('#big_img').width()+'px')
$('ul.thumbnail_list').on('mouseenter','a.thumbnail_custom',function(){
    var smallAttr = $(this).children().attr('src');
    var bigAttr = $('#big_img').attr('src');
    $('#big_img').attr('src',smallAttr);
});//缩略图展示end

/* ajax  立即购买*
--------------------------*/
/* $('.buy-now').click(function () {
    getLogin();
    if ($('.act_box').length === 0) {
        $('.table').find('.red_msg').remove();
        $('.table').append('<p class="red_msg">请选择</p>');
    } else {
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
                    productCookie();
                    window.location.href = '/bill/bills/?new';
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
}); */ 

/* 选中规格效果
--------------------------*/
$('table.table').on('click', '.rule_tr', function () {
    $(this).siblings().removeClass('act_box');
    $(this).addClass('act_box');
    $('.table').find('.red_msg').remove();
    $('.stock_copy').text($(this).children('.stock').text());
    $('#total_price').text($('.act_box').children('.unit-price').text() * $('.carnum').text());
});

/* 加 
--------------------------*/
$('.btn-group').on("click", '.addition', function () {
    var quantity = parseInt($(this).next().text());
    var nStock = parseInt($('.stock_copy').text());
    if (quantity >= nStock) {
        $(this).next().text(nStock)
    } else { $(this).next().text(quantity + 1); }
    //价格变动
     $('#total_price').text($('.act_box').children('.unit-price').text() * $('.carnum').text());
});

/* 减去 
--------------------------*/
$('.btn-group').on("click", '.subtraction', function () {
    var quantity = parseInt($(this).prev().text());
    if (quantity <= 1) {
        $(this).prev().text(1);
    } else {
        $(this).prev().text(quantity - 1);
    }
    //价格变动
    $('#total_price').text($('.act_box').children('.unit-price').text() * $('.carnum').text());
});
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
        fnRuleShow();
    } else {
        ajaxSubmit();
    }
});