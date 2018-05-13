  
var id='';
$('.refundsubmit').on('click', '.btn-approve', function () {
    var status = $(this).attr('value');
    $('#sure').attr('status', status);
    if (status == '3'){
        if ( $("#refuse_reason").val() == ''){
            $("#refuse_reason").focus();
            $().message('请填写驳回说明');
            return false;
        }
        else{
            $(".poptext").text("确定驳回退款申请？");
        }
        
    }
    $('.pop_up').show(); 
})
$('#sure').on('click',function () {//确认退货
    id = $('#billid').val();
    var status = $('#sure').attr('status');
    var refuse_reason = '';
    var $refuse_reason = $("#refuse_reason");
    if ($refuse_reason.length > 0){
        refuse_reason = $refuse_reason.val();
    }
    var data = {
        'method': 'put',
        'approve': status,
        'id': id,
        'reason':refuse_reason,
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