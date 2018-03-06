

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


    //  创建地址按钮    >>> 点击事件
    $('body').on('click','.create-btn',function(){ 
        var intemplate = $("#intemplate");//表明是嵌入式的还是非嵌入式的

        var areaid = $.trim($('#counties').val());
        var phone = $.trim($('#new_phone').val());
        var receiver = $.trim($('#receiver').val());
        var detail = $.trim($('#detail').val());
        // 验证数据有效性
        if (receiver == '') {
            $().errormessage('请填写收货人姓名');
            $('#receiver').focus();
            return;
        }
        if (phone == '') {
            $().errormessage('请填写收货人电话');
            $('#phone').focus();
            return;
        }
        if (detail == '') {
            $().errormessage('请填写收货人详细地址');
            $('#address').focus();
            return;
        }
        // 验证数据有效性 结束
        if ($("#default").is(':checked')){
            addr_default = 1;
        }else{
            addr_default = 0;
        }
        data = {
            'method': 'create',
            'areaid': areaid,
            'phone': phone,
            'receiver': receiver,
            'detail': detail,
            'default':addr_default,
            'csrfmiddlewaretoken': getCookie('csrftoken'),
        };
        var addressid = $('#addressid');
        if (addressid.length > 0) {
            //3
            data['id'] = addressid.val();
            data['method'] = 'put'; //修改 
        }

        var html = '<div class="alert alert-danger" role="alert">####</div>';
        $.ajax({
            type: 'post',
            url: '/address/addresses/',
            data: data,
            success: function (result) {
                if (result['status'] == 'ok') {
                    if (intemplate.length >= 1){
                        //嵌入式网页，在订单提交的时候
                        $.ajax({
                            type: 'get',
                            url: '/address/addresses/?template', 
                            success: function (result) {
                                $("#item-address").empty();
                                $('#addressModal').modal('toggle');
                                $("#item-address").append(result);
                            }
                        }); 
                    }
                    else{
                        $().message(result['msg']);
                        setTimeout(function () {//三秒返回
                            location.href='/address/addresses/';
                        }, 3000);
                    }
                } else {
                    $().errormessage(result['msg']);
                }
            },
            error: function () {
                // 500
                alert('server is down!')
            }
        })
    });

});
/* 
 *省份change获取市
 */
$('body').on('change','#province',function(){
//$('#province').change(function () {
    $('#city').val('');
    $.get('/area/get_city_list/?provinceid=' + this.value, function (data) {
        $('#city').empty();
        if (data.length == 1)//北京、上海、重庆、天津4个直辖市
        {
             //继续请求区：
             $('#counties').val('');
             $.get('/area/get_county_list/?cityid=' + data[0].id, function (counties) {
                 $('#counties').empty();
                 for (var i = 0; i < counties.length; i++) {
                     var oCounties = counties[i];
                     
                     $('#counties').append('<option value=' + oCounties.id + '>' + oCounties.short_name + '</option>');
                 };
             });
        }
        for (var i = 0; i < data.length; i++) {
            var oCity = data[i];
            
            $('#city').append('<option value=' + oCity.id + '>' + oCity.short_name + '</option>');
        }
        
    });

})
/* 
 *市change获取县区
 */
$('body').on('change','#city',function(){
//$('#city').change(function () {
    $('#counties').val('');
    $.get('/area/get_county_list/?cityid=' + this.value, function (data) {
        $('#counties').empty();
        for (var i = 0; i < data.length; i++) {
            var oCounties = data[i];
            
            $('#counties').append('<option value=' + oCounties.id + '>' + oCounties.short_name + '</option>');
        };
    });
});
var aAddress;
$('body').on('click','.address_wrap',function(){
    var name = $(this).find('.name').text();
    var phNumber =$(this).find('.ph_number').text();
    var sAddress =$(this).find('.s_address').text();
    var nAddressId=$(this).attr('addressid');

    aAddress ={
        'name': name,
        'phone': phNumber,
        'address':sAddress,
        'address_id':nAddressId
    };
    CookieUtil.set("aAddress", JSON.stringify(aAddress), '', "/");
    history.back();
})

/* 修改 */
$('body').on('click','.address_modify',function(){
    var url = $(this).attr('url');
    $.ajax({
        type: 'get',
        url: url, 
        success: function (result) {
            $(".modal-body").html(result);
            $('#addressModal').modal('show');
        }
    });  
//  提交订单
})

$('body').on('click','.address_new',function(){
    var url = $(this).attr('url');
    $.ajax({
        type: 'get',
        url: url, 
        success: function (result) {
            $(".modal-body").html(result);
            $('#addressModal').modal('show');
        }
    });  
//  提交订单
})