/**
 * 
 * https://www.pluralsight.com/guides/work-with-ajax-django
 * https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html
 */

$('#id_service').change(function(e){
	//alert($(this).val());
	e.preventDefault();
	var serializedData = $(this).serialize();
	var pk = $(this).val();
	//alert(pk);
	
	$.ajax({
	        type: 'POST',
			url: "{% url 'ajax-sevice' %}",
			data: serializedData,
			success: function (response) {
				// on successfull creating object
				// 1. clear the form.
				// $("#friend-form").trigger('reset');
				// 2. focus to nickname input 
				$("#id_prix").focus();
	
				// display the newly friend to table.
				var instance = JSON.parse(response["service"]);
				var fields = instance[0]["fields"];
				//$("#id_prix").text(${fields["suggested_price"]);
	    
			},
			error: function (response) {
				$("#id_prix").focus();
				// alert the error if any error occured
				//alert(response["responseJSON"]["error"]);
	        }
	})
    
})

