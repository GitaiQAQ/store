    //获取当前网页
    var loadUrl=window.location.href;
    $('.page-num').click(function(){
        var url = location.origin + location.pathname + "page=" + $(this).text();
        window.location.href = url;
        
    })
    $('#go_ahead').on('click',function(){
        var nowNmb = parseInt(loadUrl.split('page=')[1]);
        var pageNum = nowNmb+1;
        var url = location.origin + location.pathname + "page=" +pageNum;
        window.location.href = url;
    })
    $('#back_off').on('click',function(){
        var nowNmb = parseInt(loadUrl.split('page=')[1]);
        var pageNum = nowNmb-1;
        var url = location.origin + location.pathname + "page=" +pageNum;
        window.location.href = url;
        
    })
