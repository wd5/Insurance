$(function() {
    //Tabs
    $("#calc-tabs").tabs();

    //Transform standart from elements
    $(".long-select").each(function(e) {
        $(this).attr("id", "long-" + (e + 1));
        transform_select($(this));
    })

    $(".short-select").each(function(e) {
        $(this).attr("id", "short-" + (e + 1));
        transform_select($(this));
    })

    $(".style-checkbox input").each(function() {
        if ($(this).attr("checked") == true) {
            $(this).parent().addClass("on");
        }
    })

    $(".style-checkbox input").click(function() {
        $(this).parent().toggleClass("on");
        if ($(this).attr("id") == "id_unlimited_drivers")
            $("#add-driver-button").toggleClass("hide");
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


//Transform Selects into custom selects
function transform_select(selectContainer) {
    var result = "";
    var realselect = $(selectContainer).find("select");

    //read select values, write and add to container
    $(selectContainer).find("select option").each(function() {
        var text = ($(this).text());
        var value = ($(this).val());
        result += "<li rel='" + value + "'>" + text + "</li>";
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
        $(this).find(".jScrollPaneContainer").css("visibility", "visible");
    })

    $(selectContainer).find(".jScrollPaneContainer").bind("mouseleave", function() {
        $(this).css("visibility", "hidden");
    })

    $(selectContainer).find("ul li").live('click', function() {
        $(selectContainer).find(".select-text").html($(this).text());
        $(selectContainer).find("input").val($(this).text());
        realselect.val($(this).attr("rel"));
        realselect.change();
        $(this).parent().parent().css("visibility", "hidden");
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

/*Price Slider on calc step 1*/
function priceSlider(containerId) {
    var min = "0",
        max = "10000000",
        step = 100;

    $("#id_price").change(function(e) {
        $(this).parent().find("#current").html($(this).val());
    })

    containerId.slider({
        value:  $("#id_price").val(),
        min: min,
        max: max,
        step: step,

        create: function() {
            //$("#id_price").css("visibility", "hidden");
            containerId.find("a.ui-slider-handle").append("<span id='current'>0</span>");
            containerId.find("#current").html($("#id_price").val());
        },

        slide: function(event, ui) {
            $("#current").html(ui.value);
            $("#id_price").val(ui.value);
        }
    });

    containerId.parent().find("#min").html(min);
    containerId.parent().find("#max").html(max);
}


/*Franchize Slider on calc step 2*/
function franchiseSlider(selectId) {
    var sliderVal = selectId.find("select");
    var values = [];
    var min = "",
        max = "",
        step = "";

    sliderVal.find("option").each(function() {
        values.push($(this).text());
    });

    min = values[0];
    max = values[(values.length - 1)];
    step = values[1] - values[0];

    selectId.slider({
        value: selectId.find("select").val(),
        min: min,
        max: max,
        step: step,

        create: function() {
            selectId.find("a.ui-slider-handle").append("<span id='current'></span>");
            $("#current").html(selectId.find("select").val());
        },

        slide: function(event, ui) {
            $("#current").html(ui.value);
            selectId.find("select").val(ui.value);
            selectId.find("select").change();
        }
    })


    selectId.parent().find("#min").html(min);
    selectId.parent().find("#max").html(max);
}

//Show Preloader function when submit data on server
function preloaderScreen() {
    var over = $("#overlay");
    var width = $(document).width(),
        heigth = $(document).height();

    over.css({"width": width, "height" : heigth});
    over.show();
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
        } else if (text.indexOf(current_value) === 0 && !best_candidate) {
            best_candidate = $(this);
        }

    });

    if (best_candidate && !value_found) {
        scrollToItem(best_candidate);
    } else if (!best_candidate && !value_found) {

    }
}

//User type in short input value
function userTypeShortInput(input, val) {
    var current_value = (input.val()).toUpperCase();
    // console.log(current_value);
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
        } else if (text.indexOf(current_value) === 0 && !best_candidate) {
            best_candidate = $(this);
        }

    });

    if (best_candidate && !value_found) {
        scrollToItem(best_candidate);
        // console.log(best_candidate.text());
    } else if (!best_candidate && !value_found) {

    }
}

/*Highlight value in list*/
function scrollToItem(list_item) {
    list_item.parent().find("li").removeClass("selected");
    list_item.parent().find("li").not(list_item).addClass("inactive");
    list_item.addClass("selected");
    list_item.parent().css("top", -list_item.position().top);
}