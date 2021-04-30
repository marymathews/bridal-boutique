$(document).ready(function() {
	// Hide initially
    $("#range-error").hide();
    $("#search-error").hide();
    
    $("#customization").submit(function(event) {
        minVal = $("#min-price").val();
        minVal = (minVal == '') ? 0 : minVal;

        maxVal = $("#max-price").val();
        maxVal = (maxVal == '') ? 5000 : maxVal;

        searchVal = $("#search").val();
        searchVal = (searchVal == '') ? 'All' : searchVal;
        
        if(!isSearchValid(searchVal)) {
	        event.preventDefault();
	        $("#search-error").show().css({
	            'color': 'red'
	        });
	    }
	    else
	    	$("#search-error").hide();
        
	    if(!isMinMaxValid(minVal, maxVal)) {
	    	event.preventDefault();
	        $("#range-error").show().css({
	            'color': 'red'
	        });
	    }
	    else 
	    	$("#range-error").hide();

        $("#min-price").val(minVal); 
		$("#max-price").val(maxVal); 
     	$("#search").val(searchVal); 
	});
});

function isMinMaxValid(minVal, maxVal) {
	var min = parseInt(minVal);
	var max = parseInt(maxVal);
	if(min < 0 || max < 0 || min >= max)
		return false;
	return true;
}

function isSearchValid(search) {
	var reg = /^[A-Za-z]+$/;     
	if(reg.test(search))
        return true
	else 
  		return false;
}