$(function() {
    $("#info-main-driver td:odd").addClass("second");

    //Tabs
    $("#calc-tabs").tabs();


    //price slider on first calc page
    priceSlider($("#price-slider"));


    //Transform standart from elements
    $(".long-select").each(function(e) {
        $(this).attr("id", "long-" + (e + 1));
        transform_select($(this));
    })

    $(".short-select").each(function(e) {
        $(this).attr("id", "short-" + (e + 1));
        transform_select($(this));
    })


    $("#info-main-driver tr.hide").css("display", "none");

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


    //first select with auto mark
    if ($("#id_mark").val() != "") {
        $("#require-block-1").show();
    }

    //change first select
    $("#id_mark").change(function() {
        //Hide all table data, except first one
        $("#require-auto-data-first tr").not(":first").hide();

        $(".ajax-select select").each(function() {
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
    $(".visible-data div span").live('click', function() {
        var nextSelect = $(this).parents("td").find("select"),
            nextRow = $(this).parents("tr").next();
        $(this).parent().find("span").removeClass("active");
        $(this).addClass("active");
        nextSelect.val($(this).attr("rel"));
        nextSelect.change();

        if ((nextRow.index()) == 3) {
            $("#require-auto-data-first tr").show();
        } else {
            nextRow.show();
        }

    })

    //Draw all select values in frist block
    $("#require-block-1 select").each(function() {
        var id = $(this).attr("id");
        get_visible_select_data(id);
    })

    //Click on add driver button
    $("#add-driver-button").click(function(e) {
        e.preventDefault();
        var newRow = $("#info-main-driver").find("tr.hide:first");
        newRow.find("select").val("");
        newRow.find(".select-text").html(newRow.find("select option[selected]").text());
        newRow.removeClass("hide").addClass("show").show();
        $("#delete-driver-button").removeClass("hide").show();
    })

    //Click on delete driver button
    $("#delete-driver-button").click(function(e) {
        e.preventDefault();
        var lastRow = $("#info-main-driver").find("tr.show:last");
        if ($("#info-main-driver tr").not(".hide").length == 2) {
            $("#delete-driver-button").hide();
        }
        lastRow.removeClass("show").addClass("hide").hide();
    })

    //Submit data on server - step1, step2
    $("#form-step1, #sorting").submit(function() {
        preloaderScreen();
    })

    //Type into input element
    $(".long-select input").keypress(function(e) {
        if (e.keyCode == 8) {
            $(this).val("");
        }
        userTypeInput($(this));
    })

    //Clear additional drivers info
    $("#info-main-driver .hide select").val("");
})


function get_auto_data(currentname) {
    var data = {};

    if (currentname == "power") {
        //$("#id_price").val(0);

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
       // $(selectContainer).find(".select-text").html($(this).text());
        $(selectContainer).find("input").val($(this).text());
        realselect.val($(this).attr("rel"));
        realselect.change();
        $(this).parent().parent().css("visibility", "hidden");
    })

}


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

/*Price Slider*/
function priceSlider(containerId) {
    var min = "0",
        max = "5000000",
        step = 100;

    containerId.slider({
        value:  $("#id_price").val(),
        min: min,
        max: max,
        step: step,

        create: function() {
            $("#id_price").css("visibility", "hidden");
            containerId.find("a.ui-slider-handle").append("<span id='current'></span>");
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


/*Franchize Slider*/
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

//Show Preloader function
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
            scrollToItem(value_found);
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

/*Highlight value in list*/
function scrollToItem(list_item) {
    list_item.parent().find("li").removeClass("selected");
    list_item.addClass("selected");
    list_item.parent().css("top", -list_item.position().top);
}