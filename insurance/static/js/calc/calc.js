$(function() {
    $("#info-main-driver td:odd").addClass("second");
    $("#calc-tabs").tabs();
    
    //price slider
    $("#price-slider").slider({
        value: 0,
        min: 0,
        max: 1000000,
        step: 100,
        slide: function(event, ui){
            $("#id_price").val(ui.value);
            $("#price-label").html(ui.value);
        }
    });

    $("#id_price").css("visibility", "hidden");
    $("#id_price").val($("#price-slider").slider("value") );

        
    //Transform standart from elements
    $(".long-select .select-text").each(function(){
        var displayValue = $(this).parent().find("option[selected='selected']").text();
        $(this).html(displayValue);
    })

    $(".long-select select").click(function(){
       var selectedValue = $(this).val();
       var displayValue = $(this).find("option[value='"+ selectedValue +"']").text();
       $(this).parent().find(".select-text").html(displayValue);
    });

    $(".short-select .select-text").each(function(){
        var displayValue = $(this).parent().find("option[selected='selected']").text();
        $(this).html(displayValue);
    })
       

    $(".short-select select").click(function(){
       var selectedValue = $(this).val();
       var displayValue = $(this).find("option[value='"+ selectedValue +"']").text();
       $(this).parent().find(".select-text").html(displayValue);
    });

    $(".style-checkbox input").click(function(){
        $(this).parent().toggleClass("on");
        if($(this).attr("id") == "id_unlimited_drivers")
            $("#add-driver-button").toggleClass("hide");
            $("#info-main-driver tr").not(":first").val("").hide();
    })


    //first select with auto mark
    if ($("#id_mark").val() != "") {
        $("#require-block-1").show();
    }

    //change first select
    $("#id_mark").change(function() {
        $(".ajax-select select").each(function(){
            $(this).val("");
            get_visible_select_data($(this).attr("id"));
        });
        
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

    //Click on add driver button
    $("#add-driver-button").click(function(e){
        e.preventDefault();
        $("#info-main-driver").find("tr.hide:first").removeClass("hide").show();
      
    })

    //Clear additional drivers info
    $("#info-main-driver .hide select").val("");
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

