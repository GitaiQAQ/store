/* 
 * 缩略图展示
 */
$('ul.thumbnail_list').on('click','a.thumbnail_custom',function(){
    var smallAttr = $(this).children().attr('src');
    var bigAttr = $('#big_img').attr('src');
    if(smallAttr==bigAttr){
        $('#big_img').attr('src','');
    }else{
        $('#big_img').attr('src',smallAttr);
    }
    if($('#big_img').attr('src')==''){
        $('#big_img').css('display','none');
    }else{
        $('#big_img').css('display','block');
    }
});//缩略图展示end

/* ajax  立即购买*
--------------------------*/
$('.buy-now').click(function () {
    getLogin();
    if ($('.act_box').length === 0) {
        $('.table').find('.red_msg').remove();
        $('.table').append('<p class="red_msg">请选择</p>');
    } else {
        var url = '/shopcar/shopcars/';
        var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    
        var ruleid = $('.act_box').attr('ruleid')
        var quantity = parseInt($('#carnum').text());
        var data = {
            'method': 'create',
            'ruleid': ruleid,
            'num': quantity,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        }
        $.ajax({
            url: url,
            type: 'post',
            data: data,
            success: function (result) {
                if (result['status'] == 'ok') {
                    $().message(result['msg']);
                    productCookie();
                    window.location.href = '/bill/bills/?new';
                }
                else {
                    $().message(result['msg']);
                }
            },
            error: function () { // 500
                $().errormessage('server is down!');
            }
        });
    }
});