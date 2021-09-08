let file_array = Array();
let news_preview = undefined;

// Открыть форму
function open_form(form_id) {
	$("body").css("overflow", "hidden");
	$(form_id).addClass("active");
}

// Закрытие форм при клике вне
$(document).mouseup(function (e) {
	let exceptions = [$(".form-wrapper"), $("menu"), $(".alert")]

	if(!(exceptions.filter(exception => exception.has(e.target).length !== 0).length)){
		$(".form").removeClass("active");
		$("body").css("overflow-y", "scroll");
	}
});

// <=== Скрипты формы добавления новости ===>

// Добавление файлов по кнопке
function openFileDialog(fileInput){
	$(fileInput)[0].value = '';
	$(fileInput).click();
}

// Генерация представлений файла
function addFileWidget(file){
	return $(`
	<div class="file">
		<div class="file-info">
			<i class="file-${file.name.split('.')[file.name.split('.').length - 1]}"></i>
			<h4>${file.name}</h4>
		</div>
		<div class="file-btns">
			<button class="del-file" type="button"></button>
		</div>
	</div>`)[0]
}

function addNewsPreviewHandler(event){
	if(event.target.files[0] != undefined){
		news_preview = event.target.files[0]
		addNewsPreview(event.target.files[0])
	}
}

// Генерация интерфейся превью
function addNewsPreview(news_preview){
	$('#news-preview')[0].style.display = 'none' // Скрытие кнопки "Загрузить картинку"

	let btns_container = $('#news-form-btns')[0] // Определение контейнера
	let preview_widget = addFileWidget(news_preview) // Получение html-а превью

	// Фунция по клику на "крестик"
	$(preview_widget).find('.del-file')[0].onclick = function(click) {
		news_preview = undefined  // Забываем превью
		btns_container.removeChild(preview_widget) // Чистим html от превью
		$('#news-preview')[0].style.display = 'flex' // Открываем кнопку
	}
	btns_container.insertBefore(preview_widget, btns_container.firstChild) // Добавление превью
}

function addNewFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array);
	}
}

// Генерация интерфейса файла
function addNewFile(file, array){
	let container = $('#file-container')[0] // init контейнера
	let file_widget = addFileWidget(file) // Получение html файла

	// Функция по клику на "крестик"
	$(file_widget).find('.del-file')[0].onclick = function(click) {
		for(let i = 0; i < array.length; i++){
			if(array[i] == file.id){ array.splice(i, 1) }
		} 
		container.removeChild(file_widget) // Уборка html файла
	}
	container.appendChild(file_widget) // Добавление файла в контейнер
}
