let page = 1;
let file_array = Array()
let news_preview = undefined

// <=== Скрипты работы страницы ===>

// Открытие формы по нажатию на курс
$("#slider .item").click(function(event){
	$('#widgets .item').each(function(i, item){
		if(item == event.delegateTarget || item == event.target){
			$($('#widgets .form')[i]).addClass("active");
			$("body").css("overflow", "hidden");
		}
	})
});

// Закрытие форм при клике вне
$(document).mouseup(function (e) {
	let exceptions = [$(".form-wrapper"), $("menu"), $(".alert")]

	if(!(exceptions.filter(exception => exception.has(e.target).length !== 0).length)){
		$(".form").removeClass("active");
		$("body").css("overflow-y", "scroll");
	}
});


// Открыть форму
function open_form(form_id) {
	$("body").css("overflow", "hidden");
	$(form_id).addClass("active");
}

// <=== Скрипты формы добавления новости ===>

// Добавление файлов по кнопке
$('#file-button').on('click', function(){
	$('#file-input')[0].value = '';
	$('#file-input').click();
});

// Добавление картинки по кнопке
$('#news-preview').on('click', function(){
	$('#preview-input')[0].value = '';
	$('#preview-input').click();
});

// Генерация представлений файла
function addFileWidget(file){
	return $(`
	<div class="file">
		<div class="file-info">
			<i class="file-${file.name.split('.')[file.name.split('.').length - 1]}"></i>
			<h4>${file.name}</h4></div><div class="file-btns">
			<button class="del-file" type="button"></button>
		</div>
	</div>`)[0]
}

// Генерация интерфейса файла
function addNewFile(event){
	for(let i = 0; i < event.target.files.length; i++){
		let file = event.target.files[i] // Получение файла
		file_array.push(file)  // Помещение его в массив данных

		let container = $('#file-container')[0] // init контейнера
		let file_widget = addFileWidget(file) // Получение html файла

		// Функция по клику на "крестик"
		$(file_widget).find('.del-file')[0].onclick = function(click) {
			for(let i = 0; i < array.length; i++){
				if(array[i] == file.id){
					array.splice(i, 1)  // Уборка файла из массива
				}
			} 
			container.removeChild(file_widget) // Уборка html файла
		}
		
		container.appendChild(file_widget) // Добавление файла в контейнер
	}
}

// Генерация интерфейся превью
function addNewsPreview(event){
	if(event.target.files[0] != undefined){
		$('#news-preview')[0].style.display = 'none' // Скрытие кнопки "Загрузить картинку"
		news_preview = event.target.files[0] // Получение превью

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
}

function error_alert(message){
    $("#alertsContainer").append(`
    <div class='alert' data-aos="fade-left">
        <svg viewBox="0 0 448 512">
            <path opacity='0.6' d="M400 32H48A48 48 0 0 0 0 80v352a48 48 0 0 0 48 48h352a48 48 0 0 0 48-48V80a48 48 0 0 0-48-48zM224 384a32 32 0 1 1 32-32 32 32 0 0 1-32 32zm38.24-238.41l-12.8 128A16 16 0 0 1 233.52 288h-19a16 16 0 0 1-15.92-14.41l-12.8-128A16 16 0 0 1 201.68 128h44.64a16 16 0 0 1 15.92 17.59z"></path>
            <path d="M246.32 128h-44.64a16 16 0 0 0-15.92 17.59l12.8 128A16 16 0 0 0 214.48 288h19a16 16 0 0 0 15.92-14.41l12.8-128A16 16 0 0 0 246.32 128zM224 320a32 32 0 1 0 32 32 32 32 0 0 0-32-32z"></path>
        </svg>
        <p>${message}</p>
        <button onclick='$(this).parent().remove()'>×</button>
    </div>
    `)
}
