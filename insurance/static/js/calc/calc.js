$(function() {
    $("#calc-tabs").tabs();
    
    //price slider
    $("#price-slider").slider({
        value: 0,
        min: 0,
        max: 1000000,
        step: 100,
        slide: function(event, ui){
            $("#id_price").val(ui.value);
        }
    });

    $("#id_price").val($("#price-slider").slider("value") );
    
    //first select with auto mark
    if ($("#id_mark").val() != "") {
        $("#require-block-1").show();
    }

    //change first select
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
            $("#require-block-1 select").val("");
            $("#require-block-1 select").html("");
            $("#require-block-1").slideUp();
        }
    })

    //Change other ajax-selects
    $(".ajax-select select").change(function() {
         get_auto_data($(this).attr("name"));
    })


    //Click on visible data elements
    $(".visible-data span").live('click', function(){
        var nextSelect = $(this).parents("td").next().find("select");
        
        $(this).parent().find("span").removeClass("active");
        $(this).addClass("active");
        nextSelect.val($(this).attr("rel"));
        nextSelect.change();
    })

    //Draw all select values in frist block
    $("#require-block-1 select").each(function(){
        var id = $(this).attr("id");
        get_visible_select_data(id);
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
        var myclass = "";
        
        if($(this).attr("selected")){
            myclass="active";
        }

        if(text != "--------"){
            result += "<span rel='"+ value +"' class='"+ myclass +"'>" + text + "</span>"
        }

    })

    $("#" + selectId).parents("td").prev().html("").append(result);
}

