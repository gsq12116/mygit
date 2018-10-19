function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    var queryData = decodeQuery();
    var bookingId = queryData["booking_house_id"];
    $.get('/index/booking_info/?h_info_id='+ bookingId, function(data){
        var h_html = template('house-info-list', {house: data})
    $('.house-info').html(h_html)
    });
;    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
   $(".submit-btn").click(function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        if (startDate && endDate && startDate <= endDate) {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            var pData = {
                house_id:bookingId,
                begin_date:startDate,
                end_date:endDate,
                days:days,
                house_price:price,
                amount:amount
            }
            $.post('/index/order_add/', pData, function(data){
                if(data.code == 200){
                    alert("订单提交成功");
                }
                history.go(-2);
            });
        }else{
             showErrorMsg();
        }
   });
})