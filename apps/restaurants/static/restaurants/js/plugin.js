// $(document).ready(function(){
// 	var ShowForm = function(){
// 		var btn = $(this);
// 		$.ajax({
// 			url: btn.attr("data-url"),
// 			type: 'get',
// 			dataType:'json',
// 			beforeSend: function(){
// 				$('#modal-menu').modal('show');
// 			},
// 			success: function(data){
// 				$('#modal-menu .modal-content').html(data.html_form);
// 			}
// 		});
// 	};

// 	var SaveForm =  function(){
// 		var form = $(this);
// 		$.ajax({
// 			url: form.attr('data-url'),
// 			data: form.serialize(),
// 			type: form.attr('method'),
// 			dataType: 'json',
// 			success: function(data){
// 				if(data.form_is_valid){
// 					$('#menu-table tbody').html(data.menu_list);
// 					$('#modal-menu').modal('hide');
// 				} else {
// 					$('#modal-menu .modal-content').html(data.html_form)
// 				}
// 			}
// 		})
// 		return false;
// 	}
// //delete menu
// $('#menu-table').on("click",".show-form-delete",ShowForm);
// $('#modal-menu').on("submit",".delete-form",SaveForm)
// });