$(function() {
    $("#info-main-driver td:odd").addClass("second");
    
    //Tabs
    $("#calc-tabs").tabs();

    
    //price slider
    $("#price-label").html($("#id_price").val());

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

   //$("#id_price").css("visibility", "hidden");
    $("#id_price").val($("#price-slider").slider("value") );

        
    //Transform standart from elements
    $(".short-select").each(function(e){
        $(this).attr("id", "short-" + (e + 1));
        transform_select($(this));
    })

     $(".long-select").each(function(e){
        $(this).attr("id", "long-" + (e + 1));
        transform_select($(this));
    })

    $("#info-main-driver tr.hide").css("display", "none");

    $(".long-select .select-text").each(function(){
        var displayValue = $(this).parent().find("option[selected]").text();
        $(this).html(displayValue);
    })

    $(".short-select .select-text").each(function(){
        var displayValue = $(this).parent().find("select option[selected]").text();
        $(this).html(displayValue);
    })

    $(".style-checkbox input").each(function(){
         if($(this).attr("checked") == true){
            $(this).parent().addClass("on");
         }
    })
       
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
    $(".visible-data div span").live('click', function(){
        var nextSelect = $(this).parents("td").find("select");
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
        var newRow = $("#info-main-driver").find("tr.hide:first");
        newRow.find("select").val("");
        newRow.find(".select-text").html(newRow.find("select option[selected]").text());
        newRow.removeClass("hide").show();
    })

    //Type into input element
    $(".long-select input").keypress(function(e){
        if(e.keyCode == 8){
           $(this).val("");
        }

        var current_value = ($(this).val()).toUpperCase();
        var best_candidate = false;
        var value_found = false;
        var list_items = $(this).parent().find("li");

        list_items.each(function(){
            var text = $(this).text();
            //console.log(text);
        })
        
        //console.log(list_items);
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

    $("#" + selectId).parents("td").find("div").html("").append(result);
}


function transform_select(selectContainer){
    var result = "";
    var realselect = $(selectContainer).find("select");
 
   //read select values, write and add to container
   $(selectContainer).find("select option").each(function(){
       var text = ($(this).text());
       var value = ($(this).val());
       result  += "<li rel='"+ value +"'>" + text + "</li>";
   });

   $(selectContainer).find("ul").remove();
   $(selectContainer).find(".jScrollPaneContainer").remove();
   $(selectContainer).append("<ul>" + result + "</ul>");

    if($(selectContainer).attr("class") == "short-select"){
        $(selectContainer).find("ul").jScrollPane({scrollbarWidth: 57, showArrows: true});
    }else{
         $(selectContainer).find("ul").jScrollPane({scrollbarWidth: 14, showArrows: true});
    }


   //base events
   $(selectContainer).click(function(){
       $(this).find("ul").show();
       $(this).find(".jScrollPaneContainer").css("visibility", "visible");
   })

   $(selectContainer).find(".jScrollPaneContainer").bind("mouseleave", function(){
       $(this).css("visibility", "hidden");
   })

   $(selectContainer).find("ul li").live('click', function(){
       $(selectContainer).find(".select-text").html($(this).text());
       //$(selectContainer).find("input").val($(this).text());
       realselect.val($(this).attr("rel"));
       realselect.change();
       $(this).parent().parent().css("visibility", "hidden");
   })
    
}


//User type in input value
function userTypeInput(){
    
}