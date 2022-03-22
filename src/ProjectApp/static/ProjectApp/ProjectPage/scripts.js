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

function drop(event) {
    event.preventDefault();

    let board = event.target.closest('.board__sectionTasks');
    let task = $(`#${event.dataTransfer.getData("task")}`);
    
    $(board).append(task);
    task.attr('id', '');
}

function addTaskFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array, "#editFileContainer");
	}
}

function createOrUpdate(array, element){
    array.indexOf(element) === -1 ? array.push(element) : array.splice(array.indexOf(element), 1)
}
