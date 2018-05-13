

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

   

});
/* 
 *省份change获取市
 */
$('body').on('change', '#province', function () {
    //$('#province').change(function () {
    $('#city').val('');
    $.get('/area/get_city_list/?provinceid=' + this.value, function (data) {
        $('#city').empty();
        //if (data.length == 1)//北京、上海、重庆、天津4个直辖市
        //{
            //继续请求区：
            $('#counties').val('');
            $.get('/area/get_county_list/?cityid=' + data[0].id, function (counties) {
                $('#counties').empty();
                for (var i = 0; i < counties.length; i++) {
                    var oCounties = counties[i];

                    $('#counties').append('<option value=' + oCounties.id + '>' + oCounties.short_name + '</option>');
                };
            });
       // }
        for (var i = 0; i < data.length; i++) {
            var oCity = data[i];

            $('#city').append('<option value=' + oCity.id + '>' + oCity.short_name + '</option>');
        }

    });

})
/* 
 *市change获取县区
 */
$('body').on('change', '#city', function () {
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


/* 删除 */
$('.delete').on('click',function(){

    var thisLit=$(this);
    var data = {
        'method': 'delete',
        'id' : thisLit.parents('tr').attr('addressid'),
        'csrfmiddlewaretoken': getCookie('csrftoken')
    };
    var html = '<div class="alert alert-danger" role="alert">####</div>';
    $.ajax({
        type: 'post',
        url: '/address/addresses/',
        data: data,
        success: function (result) {
            if (result['status'] == 'ok') {
                $().message(result['msg']);
                thisLit.parents('tr').remove();//如果返回成功删除按钮的祖父元素
            } else {
                $().errormessage(result['msg']);
            }
        },
        error: function () {
            // 500
            alert('server is down!')
        }
    })
})

 //  创建地址按钮    >>> 点击事件
 $('body').on('click', '.create-btn', function () {
    var intemplate = $("#intemplate");//表明是嵌入式的还是非嵌入式的
    var areaid = $.trim($('#counties').val());
    var phone = $.trim($('#phone').val());
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
    if ($("#default").is(':checked')) {
        addr_default = 1;
    } else {
        addr_default = 0;
    }
    var data = {
        'method': 'create',
        'areaid': areaid,
        'phone': phone,
        'receiver': receiver,
        'detail': detail,
        'default': addr_default,
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
                $().message(result['msg']);
                setTimeout(function () {//三秒返回
                    location.href = '/address/addresses/';
                }, 3000);
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