/* 
 *生成预约服务号
 */

mark = false;
$('#delete').click(function(){
    //loading
    if (mark == true) {
        return;
    } 
    var aftersalsesid = $(this).attr('aftersalsesid');
    data = {
        'method': 'delete',
        'aftersalsesid': aftersalsesid, 
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

$('#confirm-delete').on('click', '.btn-ok', function(e) {
    var aftersalsesid = $(this).attr('aftersalsesid');
    var data = {
        'method': 'delete',
        'aftersalsesid': aftersalsesid, 
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
      
    $.ajax({
        type: 'post',
        url: '/aftersales/aftersales/',
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
/*
$('.aftersales-delete').click(function(){
    var aftersalsesid = $(this).attr('aftersalsesid');
    $(".confirm-delete").attr('aftersalsesid') = aftersalsesid;
});
*/
$('#confirm-delete').on('show.bs.modal', function(e) {
    //将列表中的id属性加到弹出框的确认按钮中
    $(this).find('.btn-ok').attr('aftersalsesid', $(e.relatedTarget).attr('aftersalsesid'));
});