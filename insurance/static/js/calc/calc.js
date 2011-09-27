$(function() {
    $("#calc-tabs").tabs();

    //first select with auto mark
    if ($("#id_mark").val() != "") {
        $("#require-block-1").show();
    }

    $("#id_mark").change(function() {
        if ($("#id_mark").val() != "") {
            $("#require-block-1").slideDown();
            $.ajax(
                {
                    url: model,
                    data: {mark: $(this).val()},
                    dataType:"json",
                    success:function(data) {
                        var options = '';
                        options += '<option value="">' + '--------' + '</option>';
                        $.each(data, function(index, value) {
                            options += '<option value="' + index + '">' + value + '</option>';
                        });
                        $("#id_model").html(options);
                        get_visible_select_data("id_model");
                    }
                }
            );
        } else {
            $("#require-block-1").slideUp();
        }
    })

    //Change other ajax-selects
    $("#require-auto-data-first select").change(function() {
        get_auto_data($(this).attr("name"));
    })
})


function get_auto_data(currentname) {
    var data = {};

    if (currentname == "power") {
        $("#id_price").val("");
        
        $.ajax(
            {
                url: price,
                data:{power:$("#id_power").val()},
                dataType:"text",
                success:function(data) {
                    if (data == "") {
                        $("#stoim").html("");
                    }
                    else {
                        $("#stoim").html("Стоимость должна быть " + data);
                    }
                }
            }
        );
    } else {
        var next = $("select[name='" + currentname + "']").parents("tr").next("tr").find("select").attr("name");
        var nextID = $("select[name='" + next + "']").attr("id");
        if (currentname == "model_year") {
            data['model'] = $("#id_model").val();
            data['year'] = $("#id_model_year").val();
        } else {
            data[currentname] = $("select[name='" + currentname + "']").val();
        }

        $.ajax(
            {
                url: window[next],
                data: data,
                dataType:"json",
                success:function(data) {
                    var options = '';
                    options += '<option value="">' + '--------' + '</option>';
                    $.each(data, function(index, value) {
                        options += '<option value="' + index + '">' + value + '</option>';
                    });
                    $("select[name='" + next + "']").html(options);
                    get_visible_select_data(nextID);
                }
            }
        );


    }

}

function get_visible_select_data(selectId){
    var result = "";
    
    $("#" +selectId + " option").each(function(e){
        var text = ($(this).text());
        var value = ($(this).val());
        if(e != 0){
            result += "<span rel='"+ value +"'>" + text + "</span>"
        }

    })

    $("#" + selectId).parents("td").prev().html("").append(result);
}