// insurance calculator form code

// ===== GLOBAL VARIABLES =====
var PRICE_MIN = 799000;
var PRICE_MAX = 883000;
var PRICE_STEP = 50;

function calc_form_marks_populate() {
    dbgFuncCall('calc_form_marks_populate()');
    var name = '';
    var out_str = '<option value="1000">Марка автомобиля...</option>';
    for(var mark_id in marks) {
	mark_name = marks[mark_id].name;
	out_str +=       '<option value="' + mark_id +
	    '">' + mark_name + '</option>\n';
    }
    $("#id_marks").empty();
    $("#id_marks").append(out_str);

    dbgFuncReturn();
}

function calc_form_models_populate(mark_id) {
    dbgFuncCall('calc_form_models_populate()');
    if(mark_id == '') {
	// Select empty value for mark. Clean models and years fields
	$("#id_models").empty();
	$("#id_years").empty();
	dbgFuncReturn();
	return(0);
    }
    models_id_arr = marks[mark_id].models;
    var model_id;
    var model_name;
    var out_str = '<option value="" selected>-</option>';
    for(var i = 0; i < models_id_arr.length; i++) {
	model_id = models_id_arr[i];
	model_name = models[model_id].name;
	out_str +=       '<option value="' + model_id +
	    '">' + model_name + '</option>"\n';
    }
    $("#id_models").empty();
    $("#id_models").append(out_str);
    dbgFuncReturn();
    return(true);
}

function calc_form_years_populate(model_id) {
    dbgFuncCall('calc_form_years_populate()');
    if(model_id == '') {
	$("#id_years").empty();
	dbgFuncReturn();
	return(0);
    }
    years_id_arr = models[model_id].years;
    var year_id;
    var year;
    var out_str = '<option value="" selected>-</option>';
    for(var i = 0; i < years_id_arr.length; i++) {
	year_id = years_id_arr[i];
	year = years[year_id];
	out_str +=       '<option value="' + year_id +
	    '">' + year + '</option>"\n';
    }
    $("#id_years").empty();
    $("#id_years").append(out_str);
    dbgFuncReturn();
    return(true);
}

function calc_form_marks_selection_handler() {
    dbgFuncCall('calc_form_marks_selection_handler()');
    calc_form_models_populate($(this).val());
    dbgFuncReturn();
    return(true);
}

function calc_form_models_selection_handler() {
    dbgFuncCall('calc_form_models_selection_handler()');
    $("#id_models option:selected").
	each(function() {
		 calc_form_years_populate($(this).val());
	     });
    dbgFuncReturn();
    return(true);
}

function set_form_from_post() {
    dbgFuncCall('set_form_from_post');
    if (window.mark) {
	$('#id_marks').val(window.mark);
	calc_form_models_populate(window.mark);
    }
    dbgFuncReturn();
}

function set_form_from_get() {
    dbgFuncCall('set_form_from_get');
    if (window.get_data) {
	if (window.get_data.mark) {
	    $('#id_marks').val(window.get_data.mark);
	    calc_form_models_populate(window.get_data.mark);
	}
	if (window.get_data.model) {
	    $('#id_models').val(window.get_data.model);
	    calc_form_years_populate(window.get_data.model);
	}
	if (window.get_data.model_year) {
	    $('#id_years').val(window.get_data.model_year);
	}
	if (window.get_data.weel) {
	    $('#id_weel').val(window.get_data.weel);
	}
	if (window.get_data.power) {
	    $('#id_power').val(window.get_data.power);
	}
	if (window.get_data.city) {
	    $('#id_city').val(window.get_data.city);
	}
	if (window.get_data.price) {
	    $('#id_price').val(window.get_data.price);
	    set_price_slider_value_from_form();
	}
	if (window.get_data.credit) {
	    if(window.get_data.credit == 'true') {
		$('#id_credit').attr('checked', true);
	    } else {
		$('#id_credit').attr('checked', false);
	    }
	}
	if (window.get_data.age) {
	    $('#id_age').val(window.get_data.age);
	}
	if (window.get_data.experience_driving) {
	    $('#id_experience_driving').val(window.get_data.experience_driving);
	}
    }
    dbgFuncReturn();
    return(true);
}

function set_price_slider() {
    dbgFuncCall('set_slider()');
    $("#calc_price").slider({ min:PRICE_MIN ,max: PRICE_MAX,step: PRICE_STEP });
    $( "#calc_price" ).slider({
				  slide: function(event, ui) {
				      var slider_val = $("#calc_price").slider("option","value");
				      $('#id_price').val(slider_val);
				  }
			      });
    dbgFuncReturn();
    return(true);
}

function set_price_slider_value_from_form() {
    dbgFuncCall('set_price_slider_value_from_form');
    var value = $('#id_price').val();
    $("#calc_price").slider("value",value);
    dbgFuncReturn();
    return(true);
}

$(document).ready(function() {
		      set_price_slider();
		      set_price_slider_value_from_form();
		      calc_form_marks_populate();
		      if(request_type == "GET") {
			  set_form_from_get();
		      } else {
			  set_form_from_post();
		      }

		      var params = {
			  changedEl: ".select_style select",
			  visRows: 5,
			  scrollArrows: true
		      };

		      cuSel(params);

		      // <!-- VlK: change handler should be installed after custom select init -->
		      $("#id_marks").change(calc_form_marks_selection_handler);
		      $("#id_models").change(calc_form_models_selection_handler);


		      // set_form_from_get();

});
