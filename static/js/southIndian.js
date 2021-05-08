$(document).ready(function() {
	$('.del-btn').on('click', function(e) {
		var id = this.id;
		var form_id = "#south-indian-delete-".concat(id);
		$(form_id).attr('action','/product/'.concat(id)).submit();
	});
})