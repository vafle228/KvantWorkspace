let file_array = Array();
let participants = Array();


function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    if ($(event.target).hasClass('task')){
        event.dataTransfer.setData("task", "dragged");
        $(event.target).attr('id', "dragged");
    }
}

function addTaskFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array, "#editFileContainer");
	}
}
