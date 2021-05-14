let page = 0;
let file_array = Array()
let news_preview = undefined

// Открытие формы по нажатию на курс
$("#widgets .item").click(function(event){
	$('#widgets .item').each(function(i, item){
		if(item == event.target.parentElement || item == event.target){
			$('#widgets .form')[i].style.display = 'block';
			$("body").css("position", "fixed");
		}
	})
});

// Добавление файлов по кнопке
$('#file-button').on('click', function(){
	$('#file-input')[0].value = '';
	$('#file-input').click();
});

// Добавление картинки по кнопке
$('#news-preview').on('click', function(){
	$('#preview-input')[0].value = ''
	$('#preview-input').click()
});

// Закрытие формы
function close_form(bg) {
	bg.parentElement.style.display = 'none';
	$("body").css("position", "relative");
}

// Открытие формы создания новости
function open_add_news_form() {
	$('#news #add-news-form')[0].style.display = 'block';
	$("body").css("position", "fixed");
}

// Генерация представлений файла
function addFileWidget(file){
	return $(`<div class="file"><div class="file-info">
			  <i class="file-${file.name.split('.')[file.name.split('.').length - 1]}"></i>
			  <h4>${file.name}</h4></div><div class="file-btns">
			  <button class="del-file" type="button"></button></div></div>`)[0]
}

// Генерация интерфейса файла
function addNewFile(event){
	if(event.target.files[0] != undefined){
		let file = event.target.files[0] // Получение файла
		file_array.push(file)  // Помещение его в массив данных
		let file_id = file_array.length - 1

		let container = $('#file-container')[0] // init контейнера
		let file_widget = addFileWidget(file) // Получение html файла

		// Функция по клику на "крестик"
		$(file_widget).find('.del-file')[0].onclick = function(click) {
			file_array.splice(file_id, 1)  // Уборка файла из массива
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
		console.log()

		// Фунция по клику на "крестик"
		$(preview_widget).find('.del-file')[0].onclick = function(click) {
			news_preview = undefined  // Забываем превью
			btns_container.removeChild(preview_widget) // Чистим html от превью
			$('#news-preview')[0].style.display = 'block' // Открываем кнопку
		}

		btns_container.insertBefore(preview_widget, btns_container.firstChild) // Добавление превью
	}
}

// Генерация новости
function buildNews(news){
	return $(`<div class="item" onclick="location.href='/news/${user_id}/detail/${news.id}'">
			  <img src="${news['image']}" class="preview"><div class="item-header"><div class="news-title">
			  <h2>${news['title']}</h2></div><div class="news-author"><h4>${news['author']['name']}</h4>
			  <img src="${news['author']['img']}" class="profile-img"></div></div>
			  <p>${news['content']}</p><div style="display: flex; margin-left: auto; align-items: center;">
	   		  <span><h5 style="display: inline-block;">${news['date']}</h5></span>
	   		  <span class="fi-rr-calendar" style="font-size: 0.8rem; margin-left: 5px;"></span></div></div>`)[0]
}

// Запрос новостей с сервера
function getNewNews(){
	$.ajax({
		type: 'POST',
		url: send_news,
		data: {
			page: page,
			csrfmiddlewaretoken: csrf_token,
		},
		cache: false,
		success: function(response){
			for(let i in response['news']){ 
				$('#news-block').append(buildNews(response['news'][i]))
			}
		}
	})
	page++
	if(page * 6 >= max_news){
		$('#more-news')[0].style.display = 'none';
	}
}

// Отправка формы новости на сервер
$('#news-upload').on('click', function(){
	let news_form = new FormData();

	for(let i = 0; i < file_array.length; i++){ // Перебор файлов
		news_form.append('files', file_array[i]) // Добавление файла в форму
	}

	news_form.append('image', news_preview) // Превью
	news_form.append('content', quill.getText()) // Текст
	news_form.append('csrfmiddlewaretoken', csrf_token) // csfr_token
	news_form.append('title', $('#news-title')[0].value) // заголовок
	news_form.append('style_content', $('.ql-editor')[0].innerHTML) // форматированный текст

	$.ajax({
		type: 'POST',
		url: create_news,
		data: news_form,
		cache: false,
		processData: false,
    	contentType: false,
		enctype: "multipart/form-data",
		success: function(response) { 
			location.href = response 
		}
	})
});
