$('#back').click(function () {
    window.location.href = '/bill/bills/?unpayed';
})
$(function () {
    var inquireAbout = setInterval(
        function() {
            var billno = $('#billno').text(),
            data={
                'billno':billno
            }
            $.ajax({
                type: 'get',
                url: '/pay/weixin/',
                data:data,
                success: function (data) {
                    console.log(data);
                    if (data['status'] != 'ok')  {
                        $().errormessage(data['msg']);
                        clearInterval(inquireAbout);//停止查询
                    }
                },
                error: function () {
                    $().errormessage(data['status']);
                    clearInterval(inquireAbout);//停止查询
                }
            })  
        }
        , 1000);
    //请求服务器检查状态

})

