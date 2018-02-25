
　

$('#sel-category').change(function() {
    var categoryid = $(this).val();  
    window.location.href = '/product/products/?new&categoryid='+categoryid;
});
//  发表+存稿按钮    >>> 点击事件
$('.btn-delete ').click(function () {
    //loading样式
    var options = {
        theme: "sk-doc",
        message: '提交中...',
        backgroundColor: "#000",
        textColor: "white"
    };
    HoldOn.open(options);//loadding函数调用 
    var product = $('#productid');
      
    data = {
        'method': 'delete',
        'id':product.val(),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
  
    var html = '<div class="alert alert-danger" role="alert">####</div>';
    $.ajax({
        type: 'post',
        url: '/product/products/',
        data: data,
        success: function (result) {
            HoldOn.close();
            location.href="/product/products/";
        },
        error: function () {
            HoldOn.close();
            // 500
            alert('server is down!')
        }
    })
});

