/* 
 *返回按钮
 */
$('.back').click(function () {
    history.back();
});
/* 
 *列表最后一项去边框
 */
$('.address>div').last().css({'border':'0px'});
/* 
 *服务器加载获取省份
 */
$(document).ready(function () {
    $.get('/area/get_provice_list/', function (data) {
        for (var i = 0; i < data.length; i++) {
           var oProvince = data[i];
            $('#province').append('<option value=' + oProvince.id + '>' + oProvince.short_name + '</option>');
        };
        
    });

    //zhaji25

    //  创建地址按钮    >>> 点击事件
$('.create-btn').click(function() {
    var areaid = $.trim($('#counties').val());
    var phone = $.trim($('#phone').val());
    var receiver = $.trim($('#receiver').val());
    var detail = $.trim($('#detail').val()); 
    // 验证数据有效性
    if (receiver == ''){
        $().errormessage('请填写收货人姓名');
        $('#receiver').focus();
        return;
    }
    if (phone == ''){
        $().errormessage('请填写收货人电话');
        $('#phone').focus();
        return;
    }
    if (detail == ''){
        $().errormessage('请填写收货人详细地址');
        $('#address').focus();
        return;
    }
    // 验证数据有效性 结束

    data = {
        'method': 'create',
        'areaid': areaid,
        'phone': phone,
        'receiver': receiver,
        'detail': detail, 
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    var addressid = $('#addressid');
    if (addressid.length > 0){
        //3
        data['id'] = addressid.val();
        data['method'] = 'put'; //修改 
    }

    var html = '<div class="alert alert-danger" role="alert">####</div>';
    $.ajax({
        type: 'post',
        url: '/address/addresses/',
        data: data,
        success: function(result) {
            if (result['status'] == 'ok'){
                $().message(result['msg']);
            }else{
                $().errormessage(result['msg']);
            }
        },
        error: function() {
            // 500
            alert('server is down!')
        }
    })
});

});
/* 
 *省份change获取市
 */
$('#province').change(function(){
    $('#city').text('');
    $.get('/area/get_city_list/?provinceid='+this.value, function (data) {
        for (var i = 0; i < data.length; i++) {
            var oCity = data[i];
            $('#city').append('<option value=' + oCity.id + '>' + oCity.short_name + '</option>');
        };
    });
    
})
/* 
 *市change获取县区
 */
$('#city').change(function(){
  $('#counties').text('');
    $.get('/area/get_county_list/?cityid='+this.value, function (data) {
        for (var i = 0; i < data.length; i++) {
            var oCounties = data[i];
            $('#counties').append('<option value=' + oCounties.id + '>' + oCounties.short_name + '</option>');
        };
    });
    
})
