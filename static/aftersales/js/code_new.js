/* 
 *生成预约服务号
 */

mark = false;
$('#generate').click(function(){
    //loading
    if (mark == true) {
        return;
    } 
    if ($('#phone').val() == ''){
        $().errormessage("请输入手机号码"); 
        $('#phone').focus();
        return;
    }
    data = {
        'method': 'create',
        'address': $('#address').val(),
        'phone': $('#phone').val(),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    mark = true;
    $.ajax({
        type: 'post',
        url: '/aftersales/maintaincode/',
        data: data,
        success: function (result) {
            if (result['status'] == 'ok') { 
                    $().message(result['msg']);
                    setTimeout(function() {
                        location.reload();
                    }, 3000);
            } else {
                    $().errormessage(result['msg']);
            } 
             
        },
        error: function () {
            // 500
            alert('server is down!')
            mark = false;
            // unloading
        }

    });  
});
