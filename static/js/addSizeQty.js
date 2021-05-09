$(document).ready(function() {
	$(".click-msg").hide();
	$('.add-entry').on('click',function(e){
		e.preventDefault();
		var size = $("#add-item-dropdown").val();
		var quantity = $("#add-item-quantity").val();
		$("#add-items-list").append('<input type="text" name=size'+size+' id="'+size+'" class="size-info size-new" value="Size:'+ size + ' Quantity:'+quantity+'" readonly/>');
		$("#add-item-dropdown option[value='"+size+"']").remove();
	});

	$("ul").on("click", "input", function() {
		var size_id = '#'+this.id;
		$(size_id).remove();

		if ( $('ul').find('input').length === 0) 
			$(".click-msg").hide();
        $('#add-item-dropdown')
         	.append($("<option></option>")
         	.attr("value",this.id)
         	.text(this.id));
    });

    $("#add-items-list").on("mouseover", function() {
		$(".click-msg").show();
    });
	$("#add-items-list").on("mouseout", function() {
		$(".click-msg").hide();
    });

	$('.new-entry').on('click', function(e) {
		e.preventDefault();
		var id = 0;
		var newinput = function() {
  			var field = document.createElement("input");
  			field.id = "input" + id;
  			$('.size-qty').appendChild(field);
  			id += 1;
		}
	});
});