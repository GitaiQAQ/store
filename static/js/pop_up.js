/* 弹出框 */
$('#continue').click(function(){//点击灰色按钮关闭弹窗
    $('.pop_up').hide();
})
function pop_upMsg(msg){//显示弹出框，写入信息
    $('.pop_up').show();
    $('#pop-up-msg').text(msg);
}