    //获取当前网页
    var loadUrl=window.location.href;
   
    $('.page-num').click(function(){
        
        //去掉原来有的page=
        var url = search_url();
        console.log(url);
        if (url.indexOf('?') >= 0){
            url += "&page=" + $(this).text() ;
        }
        else{
            url += "?page=" + $(this).text() ;
        } 
        window.location.href = url;
        
    })
    $('#go_ahead').on('click',function(){
        //下一页
        console.log(loadUrl)
        var nowNmb = parseInt($(this).attr('page'));
         
        var maxNmb = parseInt($(this).attr('maxpage')); //最大页码 
        var pageNum;
        if (isNaN(nowNmb)){
            pageNum = 2;
        } 
        else{ 
         pageNum = nowNmb+1;
        }
        if (pageNum >= maxNmb){
            pageNum = maxNmb;
        }
        var url = search_url();
       

        if (url.indexOf('?') >= 0){
            url += "&page=" +pageNum;
        }
        else{
            url += "?page=" + pageNum;
        } 
 
        window.location.href = url;
    });
    $('#back_off').on('click',function(){
        //上一页
        var nowNmb = parseInt($(this).attr('page'));
       
        var pageNum = nowNmb-1;
        var pageNum;
        if (isNaN(nowNmb)){
            pageNum = 1;
        } 
        else{ 
         pageNum = nowNmb - 1;
        }
        if (pageNum <= 0)
        {
            pageNum = 1;
        }
        var url = search_url();
        if (url.indexOf('?') >= 0){
            url += "&page=" +pageNum;
        }
        else{
            url += "?page=" + pageNum;
        } 
        window.location.href = url;
        
    })

    function search_url(){
        //移除地址栏中已经有的page=的参数
        loadUrl = loadUrl.replace(/&page=[0-9]/g,'');
        loadUrl = loadUrl.replace(/\?page=[0-9]/g,'');
        return loadUrl;
    }
