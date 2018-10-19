function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $("#form-house-image").css("display", "none");
    $.get('/user/area_info/', function(data){
        var area_str = '';
        for (var i=0; i< data.area_infos.length; i++){
            area_str += "<option value='"+ data.area_infos[i].id +"'>"+ data.area_infos[i].name + "</option>";
        }
        $("#area-id").html(area_str);

        var facility_str = '';
        for (var j=0; j< data.facility_infos.length; j++){
            facility_str += "<li><div class='checkbox'><label><input type='checkbox' name='facility' value='"+ data.facility_infos[j].id +"'>"+ data.facility_infos[j].name +"</label></div></li>"
        }
        $(".house-facility-list").html(facility_str);
    });
    $("#form-house-info").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/user/newhouse/',
            type: 'POST',
            dataType: 'json',
            traditional: true,
            success: function(data){
                if (data.code == 200){
                    $("#form-house-info").hide();
                    $("#form-house-image").css("display", "block");
                    $("#house-id").val(data.house_id);
                }
            },
            error: function(data){
                alert('请求失败');
            }
        });
    });

    $("#form-house-image").submit(function(e){
        e.preventDefault();
        $('.popup_con').fadeIn('fast');
        $(this).ajaxSubmit({
            url: '/user/newhouse/',
            type: 'PATCH',
            dataType: 'json',
            success: function(data){
                if (data.code == 200){
                    $(".house-image-cons").append("<img src='/static/media/"+ data.house_image +"'>");
                }
                if (data.code == 2000){
                    alert('图片类型有误，请上传正确的格式数据');
                }
            },
            error: function(data){
                alert('请求失败');
            }
        });
        $('.popup_con').fadeOut('fast');
    });
});