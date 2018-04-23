$('#back').click(function () {
    window.location.href = '/bill/bills/?unpayed';
})
$('.qr-code').load(function () {
    var inquireAbout = setInterval(inquireAbout(), 1000);
    //请求服务器检查状态
function inquireAbout() {
    var billno = $('#billno').text();
    $.ajax({
        type: 'get',
        url: '/pay/weixin/',
        billno:'billno',
        success: function (data) {
            console.log(data);
            if (data['status'] == 'ok') {
                $().message(data['status']);
                clearInterval(inquireAbout);//停止查询
            } else {
                $().errormessage(data['msg']);
            }
        },
        error: function () {
            $().errormessage(data['status']);
        }
    })
}
})

