function getLogin() {
    var nVal = $('#userlogin').val();
    if (nVal == 0) {
        var nexturl = window.location.pathname;
        setTimeout(function () { 
            window.location.href = '/users/login/'+'?next='+nexturl;
        }
            , 2000
        );
    };
}

