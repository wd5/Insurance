$(document).ready(function(){

	var deg=90; /* ��������� ����, ��� 0 */

	/* Storing all the images into a variable */

	var images	= $('#stage img').removeClass('default').addClass('animationReady');
	var dim		= { width:images.width(),height:images.height()};

	
	var cnt = images.length;
	
	/* Finding the centers of the animation container: */
	var centerX = $('#stage').width()/2;
	var centerY = $('#stage').height()/2 - dim.height/2;

	function rotate(step,total){
		// This function loops through all the phone images, and rotates them
		// with "step" degrees (10 in this implementation) until total has reached 0
	
		/* Increment the degrees: */
		deg+=step;
		
		var eSin,eCos,newWidth,newHeight,q;
		var currentBubble = 0;
        var maxZ = 0;

		/* Loop through all the images: */
		for(var i=0;i<cnt;i++){
			
			/* Calculate the sine and cosine for the i-th image */
			
			q = ((360/cnt)*i+deg)*Math.PI/180;
			eSin		= Math.sin(q);
			eCos		= Math.cos(q);
			
			/*
			/	With the sine value, we can calculate the vertical movement, and the cosine 
			/	will give us the horizontal movement.
			*/
			
			q = (0.9+eSin*0.1);
			newWidth	= q*dim.width;
			newHeight	= q*dim.height;
			
			/*
			/	We are using the calculated sine value (which is in the range of -1 to 1)
			/	to calculate the opacity and z-index. The front image has a sine value
			/	of 1, while the backmost one has a sine value of -1.
			*/

            var zIndex = Math.round(80+eSin*20);
            images.eq(i).css({
				top			: centerY-10*eSin,
				left		: centerX+170*eCos,  /* ���� 100, ���������� ����� ������ */
				//opacity		: 1.0+eSin*1.0,
				marginLeft	: -newWidth/2,
				zIndex		: zIndex
			}).width(newWidth).height(newHeight);

            if (maxZ < zIndex) {
                maxZ = zIndex;
                currentBubble = i;
            }
		}

        var href = images.eq(currentBubble).parent().attr('href');
        $("#carosel-links a").hide();
        $("#tabsCarosel > .tabs").not(href).hide();
        $("#carosel-links a[name="+ href +"]").show();
        $(href).show();

        
		total-=Math.abs(step);
		if(total<=0) return false;


		// Setting the function to be run again in 40 seconds (equals to 25 frames per second):
		setTimeout(function(){rotate(step,total)},40);
	
	}
	
	// Running the animation once at load time (and moving the iPhone into view):
	rotate(10,360/cnt);

    $("#carosel-links a").hide();
	
	$('#phoneCarousel .previous').click(function(){
		// 360/cnt lets us distribute the phones evenly in a circle
	    rotate(-10,360/cnt);
	});
	
	$('#phoneCarousel .next').click(function(){
	    rotate(10,360/cnt);
    });

});