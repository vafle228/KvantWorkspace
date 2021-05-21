let page = 0;
let file_array = Array();
let filters = ['Ученик', 'Учитель', 'Группа', 'Администратор'];

// Прикрепление файлов по кнопке
$('#mail-file').on('click', function(){
	$('#file-input')[0].value = '';
	$('#file-input')[0].click();
})

// Закрыть форму
$(document).mouseup(function(event) {
	let container = $(".form-wrapper");
    if(container.has(event.target).length === 0 && event.which == 1) {
        $(".form").hide();
        $("body").css("position", "unset");
    }
});

// Открыть форму
function open_form(form_id) {
	$(form_id).show();
	$("body").css("position", "fixed");
}

// Поиск пользователя
function filterFunction(input) {
	let substr = input.value.toUpperCase();
	if (substr.trim()) {
		$('.unselected').show();

		let users = $('.unselected .user').map(function(index){
			let user = $('.unselected .user')[index]

			let name = $(user).find('h2')[0].textContent;
			let category = $(user).find('h4')[0].textContent;

			if(name.toUpperCase().indexOf(substr) !== -1 && filters.indexOf(category) !== -1){
				user.style.display = 'flex'
				return user
			} else { user.style.display = 'none'; }
		})
		
		if(users.length){ $('.unselected').show() }
		else { $('.unselected').hide(); }
	} 
	else { $('.unselected').hide(); }
}

function filter_applying(button, filter) {
	if ($(button).hasClass('active')) {
		$(button).removeClass('active');
		filters.splice(filters.indexOf(filter), 1);
	} else {
		$(button).addClass('active');
		filters.push(filter);
	}
	filterFunction($('.dropdown-input')[0]);
}

// Получение письм
function getNewMails(){
	$.ajax({
		type: 'POST',
		url: send_mail,
		data: {
			page: page,
			csrfmiddlewaretoken: csrf_token,
		},
		cache: false,
		success: function(response){
			for(let i in response['mails']){
				buildNewMail(response['mails'][i]);
			}
		}
	})
	page++
	if(page * 8 >= max_mails){
		$('#more-mails')[0].style.display = 'none'
	}
}

// Отправка письма по кнопке
$('#send-mail').on('click', function(){
	let mail_form = new FormData(); // Формирование формы

	for(let i in file_array){ // Считывание файлов
		mail_form.append('files', file_array[i])
	}

	mail_form.append('text', quill.getText()) // Текст
	mail_form.append('csrfmiddlewaretoken', csrf_token) // csfr_token
	mail_form.append('title', $('#mail-title')[0].value) // Заголовок

	$('.selected .user').map(function(index){
		let user = $('.selected .user')[index]
		mail_form.append('receiver', $(user).attr('value'))
	})
	mail_form.append('style_text', $('.ql-editor')[0].innerHTML) // Форматированный текст

	$.ajax({
		type: 'POST',
		data: mail_form,
		url: create_mail,
		cache: false,
		processData: false,
    	contentType: false,
		enctype: "multipart/form-data",
		success: function() { 
			location.reload()
		}
	})
})

// Смена статуса на "прочитанное"
function updateMailStatus(mail_id, mail){
	if(mail.className == 'item new-mail'){
		$.ajax({
			type: 'POST',
			url: change_status,
			data: {
				mail_id: mail_id,
				csrfmiddlewaretoken: csrf_token,
			},
			cache: false,
			success: function(){
				mail.className = 'item old-mail';
			}
		})
	}
}

// Построение нового письма
function buildNewMail(mail){
	let mail_view = generateMailView(mail) // Получение view письма

	// Генерация фалового блока
	if (mail['files'].length !== 0) {
		let files_container = $('<div class="files" style="width: 100%"></div>')[0]

		for(let i in mail['files']){ // Перебор всех файлов письма
			// Добавления файлового виджета
			$(files_container).append(generateMailFile(mail['files'][i]))
		}
		$(mail_view).append(files_container)
	}
	let mail_detail_view = buildMailView(mail) // Получение детального view

	mail_view.onclick = function(){ // Связь между view и детальным view письма
		mail_detail_view.style.display = 'block';
		$("body").css("position", "fixed");
		updateMailStatus(mail['id'], mail_view)
	}

	$('#mail_container')[0].appendChild(mail_view)
}

// Построение детального просмотра новости
function buildMailView(mail){
	let detail_view = generateMailDetailView(mail) // Получение детального образа

	// Генерация файлового блока
	if(mail['files'].length !== 0){
		$(detail_view).find('form')[0].append($('<hr class="divider"/>')[0]) // Линия-граница
		
		// Генерация контейнера файлов
		let file_div = $('<div class="files" style="width: 100%"></div>')[0]
		for(let i in mail['files']){  // Перебор всех файлов письма
			// Добавление файла в контейнер с добавкой кнопок "скачать"
			$(file_div).append($(generateMailFile(mail['files'][i])).append(
				$(`<div class="file-btns"><button onclick="window.open('${mail['files'][i]['url']}')" class="download-file" type="button"></button></div></div>`)[0]
			))
		}
		// Добавка всех файлов в контейнер с "оберткой"
		$(detail_view).find('form')[0].append(file_div)

	}
	$('#mail').append(detail_view)

	return detail_view
}

// Генерация простого view письма
function generateMailView(mail, is_mail){
	let mail_type = 'old-mail'
	if(!(mail.is_read)){ mail_type = 'new-mail' }
	return $(`<div class="item ${mail_type}"><div class="item-header"><div class="lesson-title">
			  <h2>${mail['title']}</h2><h3>${mail['date']}</h3></div><div class="lesson-teacher">
			  <h4>${mail['sender']['name']}</h4><img src="${mail['sender']['image']}">
			  </div></div><p class="item-text">${mail['text']}</p></div>`)[0]
}

// Генерация подробного view письма
function generateMailDetailView(mail){
	return $(`<div class="form"><div class="form-wrapper"><form><div class="item-header">
			  <div class="lesson-title"><h2>${mail['title']}</h2></div><div class="lesson-teacher">
			  <h4>${mail['sender']['name']}</h4><img src="${mail['sender']['image']}"/></div></div>
			  <div class="ql-snow"><div class="ql-editor"><p class="item-text">${mail['style_text']}</p>
			  </div></div><div class='date__container'><span class="fi-rr-calendar"></span>
			  <h5>Дата отправки ${mail['date']}</h5></div></form></div></div>`)[0]
}

// Генерация файлов письма
function generateMailFile(file, is_mail){
	return $(`<div class="file"><div class="file-info">
			  <i class="file-${file['name'].split('.')[file['name'].split('.').length - 1]}"></i>
			  <h4>${file['name']}</h4></div>`)[0]
}

// Генерация файлов в форме
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