$(document).ready(function(){
    /* 
     *获取cookid数据
     */
    var nSum_price = JSON.parse(CookieUtil.get("sum_price"));//总价格
    var aProducts = JSON.parse(CookieUtil.get("products"));//商品
    var oAdress = JSON.parse(CookieUtil.get("aAddress"));//快递地址
    
    /* 
     *显示总价
     */
    $('#sum_price').text(nSum_price);

    $('#all_sum_price').text(nSum_price);
    /* 
     *显示总件数
     *图片显示
     */
    var sum_number = 0;
    var oImg = $('img.thumbnail');
    var counter = 0;
    //for (var i = 0; i < Math.max(oImg.length,aProducts.length); i++) {
    var html = '<tr class="car-list">  '+
        '<td class="img-wrap text-center">'+
        '    <img class="img-rounded" src="#img">'+
        '</td> '+
        '<td class="shop-msg">'+
        '    <div class="carlist_name">#productname'+
        '   </div>'+
        '   <div class="rule_content grey">#rule'+
        '   </div>'+
        '</td> '+
        '<td class="w159 text-center" carid="{{car.id}}">'+
        '           <i class="fa fa-jpy" aria-hidden="true"></i>'+
        '           <span class="carprice">#num_and_price</span>'+
        '</td> '+
        '<td class="w159 text-right">'+
        '        <i class="fa fa-jpy" aria-hidden="true"></i>'+
        '       <span class="small_sum">#total_money</span>'+
        '</td> '+
    '</tr>';
    for (var i = 0; i < aProducts.length; i++) {
        tmp = html;
        
        tmp = tmp.replace("#img", aProducts[i].img );
        tmp = tmp.replace("#productname", aProducts[i].name);
        tmp = tmp.replace("#rule", aProducts[i].rule);
        tmp = tmp.replace("#num_and_price", aProducts[i].Price+' x '+ aProducts[i].num);
        tmp = tmp.replace("#total_money", aProducts[i].Price * aProducts[i].num);
        $("#tb_items").append(tmp);
        /*
        if (aProducts.length == 1) {
            $('.ware').children().remove();
            $('.ware').append('<img class="img-rounded pull-left" src="" />' +
                '<div class="pull-left">' +
                '<div class="product_name">商品名称</div>' +
                '<div class="product_rull font-grey">商品说明</div>' +
                '<div class="pull-left">' +
                '<i class="fa fa-jpy" aria-hidden="true"></i>' +
                '<span class="product_price">价格</span>' +
                '</div>' +
                '<div class="product_numb font-grey pull-right">件数' +
                '</div>' +
                '</div>')
            var aList = $('.ware');
            $(aList[i]).find('img').attr('src', aProducts[i].img);
            $(aList[i]).find('.product_name').text(aProducts[i].name);
            $(aList[i]).find('.product_rull').text(aProducts[i].rule);
            $(aList[i]).find('.product_price').text(aProducts[i].Price);
            $(aList[i]).find('.product_numb').text('x' + aProducts[i].num + '件');
        };
        if (aProducts[i]) {
            $(oImg[i]).css('display', 'block');
            sum_number += parseInt(aProducts[i].num);
            var aSrc = aProducts[i].img;
            $(oImg[i]).attr('src', aSrc);
        }
        */
    };
    $('.sum_num').text( sum_number);

    /* 
    *地址栏text
    */
    
    var addressIcon = '<i class="fa fa-map-marker" aria-hidden="true"></i>:';
    if (oAdress) {
        $('#name').text('' + oAdress.name);
        $('#phone').text('' + oAdress.phone);
        $('#address').html(' <div id="address">' + oAdress.address + '</div>');
    } else {
        $('#name').text('姓名：');
        $('#phone').text('电话：');
        $('#address').html(' <div id="address">' + addressIcon + '</div>');
    }

    $.ajax({
            type: 'get',
            url: '/address/addresses/?template', 
            success: function (result) {
                $("#item-address").append(result);
            }
        });
        
    //  提交订单
    mark = false;
    $('.submit-btn').click(function () {
        //loading
        if (mark == true) {
            return;
        }

        var timeout =  (500 * 2) * 3 /500;//3 second
        
        var options = {
            theme: "sk-doc",
            message: '提交中...',
            backgroundColor: "#000",
            textColor: "white"
        };
        HoldOn.open(options);
        mark = true;
        var items = Array();
        for (var i = 0; i < aProducts.length; i++) {
            item = {
                'ruleid': aProducts[i].ruleid,
                //'num': aProducts[i].num
                'num': 1
            }
            items.push(item);
        };
        data = {
            'method': 'create',
            'address_id': oAdress.address_id,
            'phone': oAdress.phone,
            'reciever': '大哥',
            'items': JSON.stringify(items),
            'csrfmiddlewaretoken': getCookie('csrftoken')
        };
        $.ajax({
            type: 'post',
            url: '/bill/bills/',
            data: data,
            success: function (result) {
                if (result['status'] == 'ok') {
                    //$().message(result['msg']); 
                    // 不断查询订单状态
                    billno = result['no'];
                    url = '/bill/bills/?unpayed&billno='+billno; //API
                    location.href=url; 
                }
            },
            error: function () {
                // 500
                HoldOn.close();
                alert('server is down!')
                mark = false;
                // unloading
            }

        });  

    });

    
    $('.invoice_company').hide();
    //发票：切换个人与企业
    $('.invoice_type').click(function () {
        var val = $(this).val();
        if (val == 0) {
            //代表类型为企业,需要纳税号
            $('.invoice_company').show('slow');
        }
        else {
            //代表类型为个人，不需要纳税号
            $('.invoice_company').hide('slow');
        }
    })
    
});
/* 地址框删除按钮功能 */
$('body').on('click', '.delete_address', function () {
    var delete_address = $(this),
        id = delete_address.parents('.address-wrap').attr('addressid'),
        url = '/address/addresses/';
    function deleteAddress() {
        delete_address.parents('.address-wrap').remove();
    }
    data = {
        'method': 'delete',
        'id': id,
        'csrfmiddlewaretoken': getCookie('csrftoken')
    };
    $.ajax({
        type: 'post',
        url: url,
        data: data,
        success: function (result) {
            if (result['status'] == 'ok') {
                $().message(result['msg']);
                deleteAddress();
            } else {
                $().errormessage(result['msg']);
            }
        },
        error: function () {
            // 500
            alert('server is down!')
        }
    });
}) 
/* 点击地址框，选中变红 */
$('.container-car').on('click', '.msg-list', function () {
    $('.address').removeClass('act_address');
    $('.act.orange').remove();//清楚样式
    $(this).parent().addClass('act_address');
    $(this).append('<div class="act orange"><i class="fa fa-check" aria-hidden="true"></i></div>')
})
/* $(document).ready(function(){
    $('.address:first').addClass('act_address');
}) */