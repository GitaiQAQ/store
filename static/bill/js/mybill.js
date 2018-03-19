//  提交订单
$('.delete').click(function() { 
    var billid  = $(this).attr('billid');
    data = {
        'method': 'delete', 
        'billid': billid,
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
   

    $.ajax({
        type: 'post',
        url: '/bill/bills/'+billid+'/',
        data: data,
        success: function(result) {
            $().message(result['msg']); 
            setTimeout(function() {
                location.reload();
            }, 3000);
        },
        error: function() {
            // 500
            alert('server is down!')
        }
    })
}); 