let file_array = Array();


function addBaseFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array, "#file-container");
	}
}

function openFileDialog(fileInput){
	$(fileInput)[0].value = '';
	$(fileInput).click();
}