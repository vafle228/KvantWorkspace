let event_file_array = Array();
let event_preview = undefined;

// <=== Скрипты формы добавления новости ===>

// Добавление файлов по кнопке


function addEventPreviewHandler(event){
	if(event.target.files[0] !== undefined){
		event_preview = event.target.files[0]
		addEventPreview(event.target.files[0])
	}
}

function addNewEventFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		event_file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array, "#event-file-container");
	}
}

function addEventPreview(event_preview){
	$('#event-preview')[0].style.display = 'none' // Скрытие кнопки "Загрузить картинку"

	let btns_container = $('#eventFormButtons')[0] // Определение контейнера
	let preview_widget = addFileWidget(event_preview) // Получение html-а превью

	// Фунция по клику на "крестик"
	$(preview_widget).find('#del-btn')[0].onclick = function(click) {
		event_preview = undefined  // Забываем превью
		btns_container.removeChild(preview_widget) // Чистим html от превью
		$('#event-preview')[0].style.display = 'flex' // Открываем кнопку
	}
	btns_container.insertBefore(preview_widget, btns_container.firstElementChild.nextSibling) // Добавление превью
}
