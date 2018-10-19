$(document).ready(function(){
    $(".auth-warn").show();
    $("#houses-list li:first-child").hide();
    $.get('/user/check_auth/', function(data){
        if (data.code == 200){
            $(".auth-warn").hide();
            $("#houses-list li:first-child").show();
        }
    });

    $.get('/user/my_houses/', function(data){
        if (data.code == 200){
            for(var i=0 ;i< data.houses_info.length;i++){
                $("#houses-list").append("<li><a href='/user/detail/"+
                data.houses_info[i].id +"/'><div class='house-title'><h3>房屋ID:"+
                data.houses_info[i].id +" —— "+ data.houses_info[i].title +
                "</h3></div><div class='house-content'>"+
                "<img src='/static/media/"+ data.houses_info[i].image +"'>"+
                "<div class='house-text'><ul><li>位于："+ data.houses_info[i].address +
                "</li><li>价格：￥"+ data.houses_info[i].price +"/晚</li><li>"+
                "发布时间："+ data.houses_info[i].create_time +"</li></ul></div></div></a></li>")
            }
        }
    });
})
