//  提交订单
$('.delete').click(function () {
    var billid = $(this).attr('billid');
    data = {
        'method': 'delete',
        'billid': billid,
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };


    $.ajax({
        type: 'post',
        url: '/bill/bills/' + billid + '/',
        data: data,
        success: function (result) {
            $().message(result['msg']);
            setTimeout(function () {
                location.reload();
            }, 3000);
        },
        error: function () {
            // 500
            alert('server is down!')
        }
    })
});
$('#leading_out').on('click', function (e) {
    e.preventDefault();
    var nowUrl = window.location.href;
    if (nowUrl.indexOf("?") >= 0) {
        window.location.href = nowUrl + '&print=';
    } else {
        window.location.href = nowUrl + '?print=';
    }


    // $('form.search').submit(); 
})
var id='';
$('.order-form').on('click', '#refund', function () {
    $('.pop_up').show();
    id = $(this).parents('table').find('.delete').attr('billid');
})
$('#sure').on('click',function () {//确认退货
    var data = {
        'method': 'put',
        'reason': $('textarea').val(),
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