// insurance calculator form code

function calc_form_marks_populate() {
    dbgFuncCall('calc_form_marks_populate()');
    var name = '';
    var out_str = '<option value="" selected>-</option>';
    for(var mark_id in marks) {
	mark_name = marks[mark_id].name;
	out_str +=       '<option value="' + mark_id + 
	    '">' + mark_name + '</option>"\n';
    }
    $("#calc_marks").empty();
    $("#calc_marks").append(out_str);
    dbgFuncReturn();
}

function calc_form_models_populate(mark_id) {
    dbgFuncCall('calc_form_models_populate()');
    if(mark_id == '') {
	// Select empty value for mark. Clean models and years fields
	$("#calc_models").empty();
	$("#calc_years").empty();
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
    $("#calc_models").empty();
    $("#calc_models").append(out_str);
    dbgFuncReturn();
}

function calc_form_years_populate(model_id) {
    dbgFuncCall('calc_form_years_populate()');
    if(model_id == '') {
	$("#calc_years").empty();
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
    $("#calc_years").empty();
    $("#calc_years").append(out_str);
    dbgFuncReturn();
}

function calc_form_marks_selection_handler() {
    dbgFuncCall('calc_form_marks_selection_handler()');
    $("#calc_marks option:selected").
	each(function() {
		 calc_form_models_populate($(this).val());
	     });
    dbgFuncReturn();
}

function calc_form_models_selection_handler() {
    dbgFuncCall('calc_form_models_selection_handler()');
    $("#calc_models option:selected").
	each(function() {
		 calc_form_years_populate($(this).val());
	     });
    dbgFuncReturn();
}

$(document).ready(function() {
		      dbgConsole(marks);
		      calc_form_marks_populate();
		      $("#calc_marks").change(calc_form_marks_selection_handler);
		      $("#calc_models").change(calc_form_models_selection_handler);
		  });


