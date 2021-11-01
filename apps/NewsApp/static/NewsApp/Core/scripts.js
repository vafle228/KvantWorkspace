let file_array = Array();
let news_preview = undefined;

// Открыть форму
function open_form(form_id) {
	$("body").css("overflow", "hidden");
	$(form_id).addClass("active");
}

// <=== Скрипты формы добавления новости ===>

// Добавление файлов по кнопке
function openFileDialog(fileInput){
	$(fileInput)[0].value = '';
	$(fileInput).click();
}

function addNewsPreviewHandler(event){
	if(event.target.files[0] != undefined){
		news_preview = event.target.files[0]
		addNewsPreview(event.target.files[0])
	}
}

function addNewFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array, "#file-container");
	}
}

// Генерация интерфейся превью
function addNewsPreview(news_preview){
	$('#news-preview')[0].style.display = 'none' // Скрытие кнопки "Загрузить картинку"

	let btns_container = $('#news-form-btns')[0] // Определение контейнера
	let preview_widget = addFileWidget(news_preview) // Получение html-а превью

	// Фунция по клику на "крестик"
	$(preview_widget).find('#del-btn')[0].onclick = function(click) {
		news_preview = undefined  // Забываем превью
		btns_container.removeChild(preview_widget) // Чистим html от превью
		$('#news-preview')[0].style.display = 'flex' // Открываем кнопку
	}
	btns_container.insertBefore(preview_widget, btns_container.firstChild) // Добавление превью
}