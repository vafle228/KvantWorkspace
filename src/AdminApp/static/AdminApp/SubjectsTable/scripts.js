let subject_preview = undefined;


function addProjectPreviewHandler(event){
	if(event.target.files[0] !== undefined){
		subject_preview = event.target.files[0]
		addSubjectPreview(event.target.files[0])
	}
}


// Генерация интерфейся превью
function addSubjectPreview(subject_preview){
	$('#subjectButton')[0].style.display = 'none' // Скрытие кнопки "Загрузить картинку"

	let preview_widget = addFileWidget(subject_preview) // Получение html-а превью

	// Фунция по клику на "крестик"
	$(preview_widget).find('#del-btn')[0].onclick = function(click) {
		subject_preview = undefined  // Забываем превью
		$('.modal__content')[0].removeChild(preview_widget); // Чистим html от превью
		$('#subjectButton')[0].style.display = 'flex' // Открываем кнопку
	}
	$('.modal__content').append(preview_widget) // Добавление превью
}
