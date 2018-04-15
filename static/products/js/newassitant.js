
//  规格设置    >>> 删除行
$('#tb_rule').on('click', '.fa-trash-o', function() {

    $(this).parent().parent().remove();

});

//  规格设置    >>> 添加
$('.add-rule').click(function() {
    $(".alert-text").remove();
    var rule_el = document.getElementById('tb_rule');
    var name = $('#name').val();
    var price = $('#price').val();
    var inventory = $('#inventory').val();
    var newhtml = ' <tr class="tr_rule" ruleid="-1">' +
        '<td class="name">' + name + '</td>' +
        '<td class="price">' + price + '</td>' +
        '<td class="inventory">' + inventory + '</td>' +
        ' <td><i class="fa fa-trash-o" aria-hidden="true"></i></td>' +
        ' </tr>';

    if (name.length == 0 || price.length == 0 ) {
        var html = '<div class="alert-text">内容不能为空!</div>';
        $('#tb_rule').before(html);
    } else if (isNaN(price) ) {
        var html = '<div class="alert-text">价格或库存只能输入数字!</div>';
        $('#tb_rule').before(html);
    } else {
        rule_el.innerHTML = rule_el.innerHTML + newhtml;
        $('#name,#price').val("");
    }; 
});

//  发表+存稿按钮    >>> 点击事件
$('.submit button').click(function() {
    var options = {
        theme: "sk-doc",
        message: '提交中...',
        backgroundColor: "#000",
        textColor: "white"
    };
    HoldOn.open(options);
    var categoryid = $('#sel-category').val();
    var title = $('#title').val();
    var desc = $('#desc').val();
    var detail = CKEDITOR.instances['id_detail'].getData();
    //
    var categoryid = $('#sel-category').val();
    var taobaourl = $('#taobaourl').val();
    var mail_price = $('#mailmoney').val();
    var delivery_time = $('#delivery_time').val();
    var mainrulename = $('#mainrulename').val();
    var vicerulename = $('#vicerulename').val();
    //
    
    var obj = {};
    var rules = Array();

    
    var rules_tr = $('.tr_rule');
    rules_tr.each(function() {
        //新建
        obj['name'] =$(this).find('.name').text(); 
        obj['price'] = $(this).find('.price').text(); 
        obj['inventory'] = $(this).find('.inventory').text();
        rules.push(obj);
        obj = {};
    });
    
   

    data = {
        'method': 'create',
        'categoryid': categoryid,
        'title': title,
        'mainrulename': mainrulename,
        'vicerulename': vicerulename,
        'description': desc,
        'mail_price':mail_price,
        'delivery_time': delivery_time,
        'detail': detail,
        'taobaourl' :taobaourl,
        'rules': JSON.stringify(rules), 
        'status': $(this).attr('status'),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    /*2017年11月1日18:00:35
    
    if (product.length > 0){
        //3
        data['id'] = product.val();
        data['method'] = 'put'; //修改产品
    }
    */

    var html = '<div class="alert alert-danger" role="alert">####</div>';
    $.ajax({
        type: 'post',
        url: '/product/products/',
        data: data,
        success: function(result) {
            HoldOn.close(); 
            $('.msg').append(html.replace('####', result['msg']));
        },
        error: function() {
            HoldOn.close(); 
            // 500
            alert('server is down!')
        }
    })
});
 
