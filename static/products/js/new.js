
　

$('#sel-category').change(function() {
    var categoryid = $(this).val();  
    window.location.href = '/product/products/?new&categoryid='+categoryid;
});


