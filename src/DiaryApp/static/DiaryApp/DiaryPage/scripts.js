let file_array = Array();

function sendWorkData(form, post_url, btn){
	btn.disabled = true;
	$(btn).addClass('disabled')

	$.ajax({
		type: 'POST',
		url: post_url,
		data: form,
		cache: false,
		processData: false,
		contentType: false,
		enctype: "multipart/form-data",
		success: function(response) {
			if(response.status == 400){
				
				btn.disabled = false;
				$(btn).removeClass('disabled')
				
				errorAlert(response.errors);
			}
			else{ changeTask(response.link) }
		}
	})
}


function changeTask(task_url){
	$.ajax({
		type: "GET",
		url: task_url,
		cache: false,
		success: function(response){
			$("#task").html(response);
		}
	})
}

function addWorkFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array, "#file-container");
	}
}