// Изменение вида чекбоксов
$(function() {
    $('input').ezMark();
    $('.silter_checkbox input').ezMark({checkboxCls: 'ez-checkbox-green', checkedCls: 'ez-checked-green'})
	$('input[type="radio"]').ezMark();
});	
// Разворачивание фильтров
$(document).ready(function(){
    $(".all_filter").click(function(){
        $(".filter_all").slideToggle("slow");
        $(this).toggleClass("all_filter_top");
    });
});
// Разворачивание формы р/с
$(document).ready(function(){
    $(".predoplata_info_radio").click(function(){
        $(".predoplata_info").animate({opacity: "show"}, "slow");
    });
});
$(document).ready(function(){
    $(".predoplata_info_radio_none").click(function(){
        $(".predoplata_info").animate({opacity: "hide"}, "fast");
    });
});
// Разворачивание формы способ доставки
$(document).ready(function(){
    $(".dostavka_1").click(function(){
        $(".vid_dostavki").animate({opacity: "show"}, "slow");
		$(".adres_sklada").animate({opacity: "hide"}, "fast");
    });
});
$(document).ready(function(){
    $(".dostavka_2").click(function(){
		$(".adres_sklada").animate({opacity: "show"}, "slow");
        $(".vid_dostavki").animate({opacity: "hide"}, "fast");
    });
});

// актовность кнопки оформления заказа
$(document).ready(function(){
 	$(".silter_checkbox input").change(function() { 
  		if ($(".silter_checkbox input").is(':checked')) {
   			$(".order_button").animate({opacity: "show"}, "slow");
   			$(".order_no_active_button").animate({opacity: "hide"}, "fast");
  		} else {
   			$(".order_no_active_button").animate({opacity: "show"}, "slow");
   			$(".order_button").animate({opacity: "hide"}, "fast");
  		}
 	}).change();
});
// Выделение всех чекбоксов	
$(document).ready(function(){
    $(".link_active_all_checkbox").click(function(){

        if ($(this).hasClass('active')) {
            $('input[name^="item"]').each(function() {
                $(this).removeAttr('checked');
                $(this).trigger('change');
            });

        } else {
            $('input[name^="item"]').each(function() {
                $(this).attr({"checked":"checked"});
                $(this).trigger('change');
            });
        }
        $(this).toggleClass('active');

    }); 

});

// teaxteria пропадание текста
function clearMe(el) {
	if(el.value == 'Напишите, что вам нравится/не нравится в этом товаре, опишите свой опыт.')
		el.value = '';
}
// Описание товара
$(function() {
	$("ul.tabs_tovar_info_link").tabs("div.tabs_tovar_info > .tabs_tovar_info_cont");
});
// Товар - галерея
$(function() {
	$(".min_img_tovar img").click(function() {
		if ($(this).hasClass("active")) { return; }
		var url = $(this).attr("src").replace("_t", "");
		var wrap = $("#max_img_tovar").fadeTo("medium", 0.5);
		var img = new Image();
		img.onload = function() {
			wrap.fadeTo("fast", 1);
			wrap.find("img").attr("src", url);
		};
		img.src = url;
		$(".min_img_tovar img").removeClass("active");
		$(this).addClass("active");
	}).filter(":first").click();
});
$(function() {
	$("#max_img_tovar img[rel]").overlay({effect: 'apple', mask: '#789'});
	$('#max_img_tovar img').click(function(){
		$('#overlayImageId').attr('src', $(this).attr('src'));
	 });
});
// Листалка заказа товара
var root = $("#wizard").scrollable();


// some variables that we need
var api = root.scrollable(), drawer = $("#drawer");

// validation logic is done inside the onBeforeSeek callback
api.onBeforeSeek(function(event, i) {

	// we are going 1 step backwards so no need for validation
	if (api.getIndex() < i) {

		// 1. get current page
		var page = root.find(".page").eq(api.getIndex()),

			 // 2. .. and all required fields inside the page
			 inputs = page.find(".required :input:visible").removeClass("error"), 

			 // 3. .. which are empty
			 empty = inputs.filter(function() {
				return $(this).val().replace(/\s*/g, '') == '';
			 });

		 // if there are empty fields, then
		if (empty.length) {

			// slide down the drawer
			drawer.slideDown(function()  {

				// colored flash effect
				drawer.css("backgroundColor", "#229");
				setTimeout(function() { drawer.css("backgroundColor", "#fff"); }, 1000);
			});

			// add a CSS class name "error" for empty & required fields
			empty.addClass("error");

			// cancel seeking of the scrollable by returning false
			return false;

		// everything is good
		} else {

			// hide the drawer
			drawer.slideUp();
		}

	}

	// update status bar
	$("#status .zakaz_page").removeClass("active").eq(i).addClass("active");

});