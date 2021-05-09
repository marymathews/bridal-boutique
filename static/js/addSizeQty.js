$(document).ready(function() {
	$('.add-entry').on('click',function(e){
		e.preventDefault();
		var size = $("#add-item-dropdown").val();
		var quantity = $("#add-item-quantity").val();
		$("#add-items-list").append('<input type="text" class="size-info" name=size'+size+' id="'+size+'" class="form-control size-new" value="Size:'+ size + ' Quantity:'+quantity+'" readonly/>');
		$("option[value='"+size+"']").remove();
	});

	$("ul").on("click", "input", function(){
			console.log(this.id);
			var size_id = '#'+this.id;
            $(size_id).remove();
            $('#add-item-dropdown')
         		.append($("<option></option>")
         		.attr("value",this.id)
         		.text(this.id));
    });


	$('.new-entry').on('click', function(e) {
		e.preventDefault();
		console.log("clicked new");
		var id = 0;
		var newinput = function() {
  			var field = document.createElement("input");
  			field.id = "input" + id;
  			$('.size-qty').appendChild(field);
  			id += 1;
		}
	});
});