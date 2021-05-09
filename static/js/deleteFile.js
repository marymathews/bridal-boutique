$(document).ready(function() { 
	$(".img-btn").on("click", function(e) {
		e.preventDefault();
		var name = $(".img-container").attr("name");
		console.log(name);
		var clickedName = '1' + name.substring(1);
		$(".img-container").attr("name", clickedName);
		console.log(clickedName);
	});

	$('ul li span').hide();

    $("ul").on("mouseenter", "li", function(){
    	$(this).find("span").show();
    });

    $("ul").on("mouseleave", "li", function(){
    	$(this).find("span").hide();
    });

    $('.deleteImage').click(function(){
            var img_name = this.id;
            $(this).parent("li").find(".imgTag").text("Marked for deletion");
            $('.deleted_img_info').append('<input type="hidden" class="size-info" name=removeImage_'+img_name+' id="'+img_name+'" class="form-control size-new" value="'+ img_name + '" readonly/>');
    });
});