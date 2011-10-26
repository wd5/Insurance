$(function() {
    //Tabs
/*    $("#calc-tabs").tabs({
    select: function(event, ui) {
        return false;
        var url = $.data(ui.tab, 'load.tabs');
        if( url ) {
            location.href = url;
            return false;
        }
        return true;
    }
    }); */
    $("#calc-tabs ul li a").hover(function() {$(this).parent().toggleClass("ui-state-hover")});

    $(".style-checkbox input").each(function() {
        if ($(this).attr("checked") == true) {
            $(this).parent().addClass("on");
        }
    })

    $(".style-checkbox input").click(function() {
        $(this).parent().toggleClass("on");
        if ($(this).attr("id") == "id_unlimited_drivers") {        
            $("#add-driver-button").toggleClass("hide");
            if ((!$(this).parent().hasClass("on")) && $(".short-select:visible").length > 2) {                
                $("#delete-driver-button").addClass("hide").show();
            } else {                
                $("#delete-driver-button").removeClass("hide").hide();
            };
        };       
        $("#info-main-driver tr").not(":first").val("").hide();
    })

    //Submit data on server - step1, step2
    $("#form-step1, #sorting").submit(function() {
        preloaderScreen();
    })
})


//Get data for ajax-select on first calc page
function get_auto_data(currentname) {
    var data = {};

    if (currentname == "power") {
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
                        $("#stoim").html("Стоимость должна быть " + data + " руб.");
                    }
                }
            }
        );
    } else {
        var next = $("select[name='" + currentname + "']").parents("tr").next("tr").find("select").attr("name");
        var nextID = $("select[name='" + next + "']").attr("id");
        if (currentname == "model_year" || currentname == "model") {
            data['mark'] = $("#id_mark").val();
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
                    if (nextID == "id_model") {
                        get_visible_select_data_model(nextID);
                    } else {
                        get_visible_select_data(nextID);   
                    }
                }
            }
        );
    }
}

//Draw select data on table cell, calc step 1
function get_visible_select_data(selectId) {
    var result = "";

    $("#" + selectId + " option").each(function(e) {
        var text = ($(this).text());
        var value = ($(this).val());
        var myclass = "";

        if ($(this).attr("selected")) {
            myclass = "active";
        }

        if (text != "--------") {
            result += "<span rel='" + value + "' class='" + myclass + "'>" + text + "</span>"
        }
    })

    $("#" + selectId).parents("td").find("div").html("").append(result);
}

function get_visible_select_data_model(selectId) {
    var result = "",
        i = 1,
        options = $("#" + selectId).find("option").length,
        divide = "";

    divide = Math.ceil(options / 4);

    $("#" + selectId + " option").each(function(e) {
        var text = ($(this).text());
        var value = ($(this).val());
        var myclass = "";

        if (i == 1) {
            result += "<div class='container'>";
        }

        if ($(this).attr("selected")) {
            myclass = "active";
        }

        if (value != "") {
            result += "<span rel='" + value + "' class='" + myclass + "'>" + text + "</span>";
            i++;
        }

        if (i == divide + 1) {
            result += "</div>";
            i = 1;
        }
    })
    $("#" + selectId).parents("td").find("div").html("").append(result);
}

function transform_select2(selectContainer) {
    var sel = $(selectContainer).find("select");
    sel.hide();

    var result = "";
    $("option", sel)
        .each(function() {
                  var text = ($(this).text());
                  var value = ($(this).val());
                  result += "<li rel='" + value + "' text='" + text + "'>" + text + "</li>";                  
              });
    
    $(selectContainer).find("input").val(sel.find("option[selected]").text());
    $(selectContainer).find(".select-text").html(sel.find("option[selected]").text());
    $("<ul>" + result + "</ul>").appendTo(selectContainer).hide();

    $(selectContainer).click(function() {
        $(this).find("ul").show();
    });

    $(selectContainer).find("ul li").live('click', function() {
        $(selectContainer).find(".select-text").html($(this).text());
        $(selectContainer).find("input").val($(this).text());
        sel.val($(this).attr("rel"));
        sel.change();
        $(this).parent().hide();
    });

    $(selectContainer)
        .bind("mouseleave", function() {
                  $("ul", $(this)).hide();
              }); 
}

//Transform Selects into custom selects
function transform_select(selectContainer) {
    var result = "";
    var realselect = $(selectContainer).find("select");

    //read select values, write and add to container
    $(selectContainer).find("select option").each(function() {
        var text = ($(this).text());
        var value = ($(this).val());
        result += "<li rel='" + value + "' text='" + text + "'>" + text + "</li>";
    });

    $(selectContainer).append("<ul>" + result + "</ul>");

    if ($(selectContainer).attr("class") == "short-select") {
        $(selectContainer).find("ul").jScrollPane({scrollbarWidth: 57, showArrows: true});
    } else {
        $(selectContainer).find("ul").jScrollPane({scrollbarWidth: 14, showArrows: true});
    }

    $(selectContainer).find("input").val(realselect.find("option[selected]").text());
    $(selectContainer).find(".select-text").html(realselect.find("option[selected]").text());

    //base events
    $(selectContainer).click(function() {
        $(this).find("ul").show();
        $(this).find(".jScrollPaneContainer").css("visibility", "visible").show();
//                                 console.log($(this).find(".jScrollPaneContainer"));
    })


    $(selectContainer).bind("mouseleave", function() {
        if ($(this).find("input").length == 0) {
            $(this).find(".jScrollPaneContainer").css("visibility", "hidden").hide();
        }
    });
  
    $(selectContainer).find(".jScrollPaneContainer")
        .bind("mouseleave", function() {
                  $(this).css("visibility", "hidden").hide();
              });

    $(selectContainer).find("ul li").live('click', function() {
        $(selectContainer).find(".select-text").html($(this).text());
        $(selectContainer).find("input").val($(this).text());
        realselect.val($(this).attr("rel"));
        realselect.change();
        $(this).parent().parent().css("visibility", "hidden");
    })

}

//Transform Select on first calc page into custom selects
function transform_firstSelect(selectContainer) {
    var result = "",
        realselect = $(selectContainer).find("select"),
        options = realselect.find("option").length,
        divide = "",
        inputfocus = false,
        i = 0;

    divide = Math.floor(options / 5);

    //read select values, write and add to container
    $(selectContainer).find("select option").each(function() {
        var text = ($(this).text());
        var value = ($(this).val());

        if (i == 0) {
            result += "<div>";
        }

        result += "<span rel='" + value + "' text='" + text + "'>" + text + "</span>";
        i++;

        if (i == divide + 1) {
            result += "</div>";
            i = 0;
        }
    });

    $(selectContainer).append("<div class='inner-container'>" + result + "</div>");
    $(selectContainer).find("input").val(realselect.find("option[selected]").text());

    //base events
    $(selectContainer).find("input").focus(function() {
        inputfocus = true;
    })

    $(selectContainer).find("input").blur(function() {
        inputfocus = false;
    })

    $(selectContainer).click(function() {
        $(this).find(".inner-container").show();
    })

    $(selectContainer).find(".inner-container").mouseleave(function() {
        if (!inputfocus) {
            if ($(this).parent().find("input").val() == "") {
                $(this).parent().find("input").val(realselect.find("option:eq(0)").text());
                realselect.val(realselect.find("option:eq(0)").val());
                realselect.change();
            }
            $(this).hide();
        }
    })

    $(selectContainer).find(".inner-container span").live('click', function() {

        $(selectContainer).find("input").val($(this).text()).addClass("focus");
        realselect.val($(this).attr("rel"));
        realselect.change();
        $(this).parent().parent().css("display", "none");

    })
}


//Fill data on second ajax-select, in calc step 2
function fillAjaxSelect(selectId) {
    var result = "";
    var ourSelect = $("#" + selectId);
    var parentContainer = $("#" + selectId).parent();

    ourSelect.find("option").each(function() {
        var text = ($(this).text());
        var value = ($(this).val());
        result += "<li rel='" + value + "'>" + text + "</li>";
    })

    parentContainer.find("ul").remove();
    parentContainer.find(".jScrollPaneContainer").remove();
    parentContainer.append("<ul>" + result + "</ul>");
    parentContainer.find("ul").jScrollPane({scrollbarWidth: 14, showArrows: true})
}

function priceFormat(val, unit) {
        var t_str = val.toString().split("").reverse().join(""); // reverse string
        t_str = t_str.replace(/(.{3})/g, "$1 "); // put space into every fourth place
        return t_str.split("").reverse().join("") + " " + unit; // reverse back and append unit mark
};

/*Price Slider on calc step 1*/
function priceSlider(containerId, element, min_value, max_value) {
    if (min_value == undefined) {
        var min_value = 0;
    }

    if (max_value == undefined) {
        var max_value = 10000000;
    }

    if (element == undefined) {
        var element = "#id_price";
    }

/*    $("#current").live("change", function() {
        $(element).val($(this).val());
    }) */

    containerId.slider({
        value:  $(element).val(),
        min: min_value,
        max: max_value,
        step: 1000,

        animate: true,

        create: function() {
            $(element).css("visibility", "hidden");
            $("<input type='text' value='0' id='current' maxlength='8' alt='msk'/>")
                .appendTo(containerId.find("a.ui-slider-handle"))
                .change(function() {
                           $(element).val($(this).val());
                       });
            containerId.find("#current").val(priceFormat($(element).val().toString(), ""));
//            containerId.find("a.ui-slider-handle").append("<span id='current'>" + priceFormat($(element).val(), "") + "</span>");
            
        },

        slide: function(event, ui) {
            $("#current").val(priceFormat(ui.value.toString(), ""));
//            $("#current").html(priceFormat(ui.value, ""));
            $(element).val(ui.value);
        }
    });

    containerId.parent().find("#min").html(priceFormat(min_value, "р."));
    containerId.parent().find("#max").html(priceFormat(max_value, "р."));
}


/*Franchize Slider on calc step 2*/
function franchiseSlider(selectId) {
    var sliderVal = selectId.find("select");
    var values = [];
    var min = "",
        max = "",
        step = "";

    sliderVal.find("option").each(function() {
        values.push($(this).val());
    });

    min = parseInt(values[0]);
    max = parseInt(values[(values.length - 1)]);
    step = parseInt(values[1] - values[0]);
    
    selectId.slider({
        value: sliderVal.val(),
        min: min,
        max: max,
        step: step,

        animate: true,

        create: function() {
            selectId.find("a.ui-slider-handle").append("<span id='current'></span>");
            $("#current").html(selectId.find("select").val());
        },

        slide: function(event, ui) {
            $("#current").html(priceFormat(ui.value, ""));
            selectId.find("select").val(ui.value);
            selectId.find("select").change();
        }
    })

    selectId.parent().find("#min").html(priceFormat(min, "р."));
    selectId.parent().find("#max").html(priceFormat(max, "р."));
}

//Show Preloader function when submit data on server
function preloaderScreen() {
    var over = $("#overlay");

    var overWidth = $(document).width(),
        overHeight = $(document).height();

    $("html").css("overflow", "hidden");
    over.css({"width": overWidth, "height" : overHeight});
    over.find("img").css("top", getPageScroll() + getPageHeight() / 2);
    over.show();
}


// getPageScroll() by quirksmode.com
function getPageScroll() {
    var xScroll, yScroll;
    if (self.pageYOffset) {
        yScroll = self.pageYOffset;
    } else if (document.documentElement && document.documentElement.scrollTop) {
        yScroll = document.documentElement.scrollTop;
    } else if (document.body) {// all other Explorers
        yScroll = document.body.scrollTop;
    }
    return yScroll;
}

// Adapted from getPageSize() by quirksmode.com
function getPageHeight() {
    var windowHeight
    if (self.innerHeight) { // all except Explorer
        windowHeight = self.innerHeight;
    } else if (document.documentElement && document.documentElement.clientHeight) {
        windowHeight = document.documentElement.clientHeight;
    } else if (document.body) { // other Explorers
        windowHeight = document.body.clientHeight;
    }
    return windowHeight
}

//Save input value on click enter or change event
function saveValue(input) {
    var currentVal = input.val(),
        list_items = input.parent().find("select option"),
        nowSelected = input.parent().find("select option[selected]");

    list_items.each(function() {
        var text = $(this).text();
        if (text == currentVal) {
            nowSelected.removeAttr("selected");
            $(this).attr("selected", "selected");
            $(this).parents("div").find(".jScrollPaneContainer").css("visibility", "hidden");
        }
    })
}


//User type in input value
function userTypeInput(input) {
    var current_value = (input.val()).toUpperCase();
    var best_candidate = false;
    var value_found = false;
    var list_items = input.parent().find("li");
    var list_item = input.parent().find("ul");

    list_items.each(function() {
        if (!value_found) {
            var text = $(this).text();
        }
        if (text == current_value) {
            value_found = true;
            scrollToItem($(this));
            return false;
        }
    });

    if (current_value != "") {
        var val = input.parent().find("li[text^='" + current_value + "']");
        if (val.length > 0) {
            scrollToItem(val);
        } else {
            list_item.css("top", -20);
            list_items.removeClass("inactive").removeClass("selected");
        }
    }
}


//User type in first select input value
function userTypeInputFirst(input) {
    var current_value = (input.val()).toUpperCase();
    var best_candidate = false;
    var value_found = false;
    var list_items = input.parent().find(".inner-container span");
    var list_item = input.parent().find(".inner-container");

    list_items.each(function() {
        if (!value_found) {
            var text = $(this).text();
        }
        if (text == current_value) {
            value_found = true;
            list_item.find("span").removeClass("selected");
            list_item.find("span").not($(this)).addClass("inactive");
            $(this).addClass("selected");
            return false;
        }
    });

    if (current_value != "") {
        var val = list_item.find("span[text^='" + current_value + "']");
        if (val.length > 0) {
            list_item.find("span").removeClass("selected");
            list_item.find("span").not(val).addClass("inactive");
            val.addClass("selected");
        } else {
            list_items.removeClass("inactive").removeClass("selected");
        }
    } else {
        list_items.removeClass("inactive").removeClass("selected");
    }
}

/*Highlight value in list*/
function scrollToItem(list_item) {
    list_item.parent().find("li").removeClass("selected");
    list_item.parent().find("li").not(list_item).addClass("inactive");
    list_item.addClass("selected");
    list_item.parent().css("top", -list_item.position().top);
}

/*Display real values of visual elements*/
function displaySelectValue(element){
    var currentval = element.val();

    if(element.attr("type") == "checkbox"){
        element.parent().find("a:first").addClass("active");
    }

    if(element.attr("type") == "select-one"){
        element.parent().find("a[value='"+ currentval +"']").addClass("active");
    }
}


/*Check select value by clicking on visual element - step 4*/
function selectVisualValue (element) {
    var text = element.text(),
        val = element.attr("value"),
        field = element.parent().find("select");

    if(field.length != 0){
        element.parent().find("a").removeClass("active");
        field.find("option[value='"+ val +"']").attr("selected", "selected");
        field.change();
        element.addClass("active");
    }else{
        element.parent().find("a").removeClass("active");
        field = element.parent().find("input");

        if(field.is(':checkbox')){
           if(field.attr("checked")){
                field.removeAttr("checked");
           }else{
               field.attr("checked", "checked");
           }
        }else{
            field.val(text);
        }
        element.addClass("active");
    }
}

/*Function copy input values - step 4*/
function copyInputValues(from, to){
    var valuesArr = [];

    from.each(function(){
        valuesArr.push($(this).val());
    })

    to.each(function(e){
        $(this).val(valuesArr[e]);
        $(this).removeClass("empty");
    })
}

/*Check input values on step 4*/
function checkAllINputs(){
    var currenttab = $("form#step"),
        result = false;

    currenttab.find("input:text").each(function(){
        if ($(this).parents("span, td").hasClass("blank"))
            return true;
        var placeholder = $(this).parent().find("label").text();
        if($.trim($(this).val()) == "" || $(this).val() == placeholder){
            $(this).addClass("empty");
            if($(this).attr("id") == "id_time"){
                $(this).parent().addClass("empty");
            }
        }
    })

    currenttab.find("select").each(function(){
        if($(this).val() == ""){
            $(this).parent().addClass("empty");
        }
    })

    if(currenttab.find(".empty").length > 0 ){
        result = false;
    }else{
        result = true;
    }

    return result;
}