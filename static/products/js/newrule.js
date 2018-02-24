
　
//  发表+存稿按钮    >>> 点击事件
$('.ruledelete').click(function() {
    var rulenameid = $(this).attr('rulenameid');
    

    data = {
        'method': 'delete',
        'rulenameid': rulenameid, 
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };

    $.ajax({
        type: 'post',
        url: '/product/products/',
        data: data,
        success: function(result) {
            window.location.reload();
        },
        error: function() { 
            alert('server is down!')
        }
    })
});


