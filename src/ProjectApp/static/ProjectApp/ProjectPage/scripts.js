let file_create_array = Array();
let file_update_array = Array();

let create_participants = Array();
let update_participants = Array();


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