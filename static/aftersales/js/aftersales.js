 /* 验证手机号 */
 $(function () {
    $('#myphone').blur(function () {
        var myreg =/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/;
        if (!myreg.test($(this).val())||!$(this).length==11) {
            $('#myphone').css('border-color',"#ddd");
            $().errormessage('手机号格式不正确请重新输入');
            $('#myphone').css('border-color',"#ea5014");
        }
    })
    $('input[name=email]').blur(function () {
        var myreg =/^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
        if($(this).val()==''){
            $().errormessage('email不能为空！');
            $(this).css('border-color',"#ea5014");
        }else if (!myreg.test($(this).val())) {
            $('#myphone').css('border-color',"#ddd");
            $().errormessage('请输入有效的email！');
            $(this).css('border-color',"#ea5014");
        }
    })

    $('form').submit(function(e){
      
        
        var name = $('#name').val();
        if(name==''){
            $('#name').get(0).focus();
            $().errormessage('请填写姓名...');
            e.preventDefault();
            
            return;
        }

        var email = $('#email').val();
        if(email==''){
            $('#email').get(0).focus();
            $().errormessage('请填写邮箱...');
            e.preventDefault();
            return;
        }

        var address = $('#address').val();
        if(address==''){
            $('#address').get(0).focus();
            $().errormessage('请填写回寄地址...');
            e.preventDefault();
            return;
        }
        
        var productname = $('#productname').val();
        if(productname==''){
            $('#productname').get(0).focus();
            $().errormessage('请填写产品名称...');
            e.preventDefault();
            return;
        }

        var number = $('#number').val();
        if(number==''){
            $('#number').get(0).focus();
            $().errormessage('请填写产品序列号(PSN)...');
            e.preventDefault();
            return;
        }

        var description = $('#description').val();
        if(description==''){
            $('#description').get(0).focus();
            $().errormessage('请描述故障信息...');
            e.preventDefault();
            return;
        }

        var buy_date = $('#buy_date').val();
        if(buy_date==''){
            $('#buy_date').get(0).focus();
            $().errormessage('请填写购买日期...');
            e.preventDefault();
            return;
        }
    })
})

$("#maintaince_type").change(function(){
    var msg = $(this).find(":selected").attr("msg");
    $(".showmsg").text(msg);
});

$( "#buy_date" ).datepicker({ 
    defaultDate: "+1w",
    changeMonth: true,
    changeYear: true,
    language:'zh-CN', 
    format:'yyyy-mm-dd', 
}); 
