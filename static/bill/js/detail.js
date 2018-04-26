  
var id='';
$('.refundsubmit').on('click', '.btn-approve', function () {
    $('.pop_up').show();
    
})
$('#sure').on('click',function () {//确认退货
    id = $('#billid').val();
    var data = {
        'method': 'put',
        'approve': '2',
        'id': id,
        'csrfmiddlewaretoken': getCookie('csrftoken')
    }
    $.ajax({
        type: 'post',
        url: '/bill/bills/',
        data: data,
        success: function (result) {
            if (result['status'] == 'ok') {
                $('.pop_up').hide();
                $().message(result['msg']);
                var reload=setTimeout(function(){
                    location.reload();
                },3000)
            } else {
                $('.pop_up').hide();
                $().message(result['msg']);
            } 
        },
        error: function () {
            // 500
            alert('server is down!')
        }
    })
})
/* 弹出框 */
$('#continue').click(function () {//点击灰色按钮关闭弹窗
    $('.pop_up').hide();
})