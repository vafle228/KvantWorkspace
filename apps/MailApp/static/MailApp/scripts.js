let page = 1;
let file_array = Array();
let filters = ['Ученик', 'Учитель', 'Группа', 'Администратор'];

// Прикрепление файлов по кнопке
$('#mail-file').on('click', function(){
	$('#file-input')[0].value = '';
	$('#file-input')[0].click();
})

// Закрытие меню при клике вне
$(document).mouseup(function(e) {
	let menu = $('menu');
	let form = $(".form-wrapper");
	if (form.has(e.target).length === 0 && menu.has(e.target).length === 0 && event.which == 1){
		$(".form").hide(); $("menu").hide();
		$("body").css("overflow-y", "scroll");
	}
});

// Открыть форму
function open_form(form_id) {
	$(form_id).show();
	$("body").css("overflow", "hidden");
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
		type: 'GET',
		url: send_mail + location.search + `&?page=${page}`,
		cache: false,
		success: function(response){
			$('#mail_container').append(response);
			if(page * 8 >= 2 && page !== 0){ 
				$('#more-mails')[0].style.display = 'none'; 
			}
			for(let i in response['mails']){
				// buildNewMail(response['mails'][i]);
			}
			page++
		}
	})
}

// Отправка письма по кнопке
$('#send-mail').on('click', function(){
	let mail_form = new FormData(); // Формирование формы

	for(let i in file_array){ // Считывание файлов
		mail_form.append('files', file_array[i])
	}

	mail_form.append('text', quill.getText()) // Текст
	mail_form.append('csrfmiddlewaretoken', getCookie('csrftoken')) // csfr_token
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
	if($(mail).hasClass('item new-mail')){
		$.ajax({
			type: 'POST',
			url: change_status,
			data: {
				mail_id: mail_id,
				csrfmiddlewaretoken: getCookie('csrftoken'),
			},
			cache: false,
			success: function(){
				$(mail).toggleClass('item new-mail item old-mail');
			}
		})
	}
}

function updateImportantStatus(mail_id){
	$.ajax({
		type: 'POST',
		url: change_important,
		data: {
			mail_id: mail_id,
			csrfmiddlewaretoken: getCookie('csrftoken'),
		},
		cache: false
	})
}

// Построение нового письма
function buildNewMail(mail){
	let mail_view = generateMailView(mail) // Получение view письма

	// Генерация фалового блока
	if (mail['files'].length !== 0) {
		let container_class = 'file'
		if(mail['files'].length > 2){ container_class = 'file file-mini' }

		let files_container = $('<div class="files" style="width: 100%"></div>')[0]

		for(let i in mail['files']){ // Перебор всех файлов письма
			// Добавления файлового виджета
			$(files_container).append(generateMailFile(mail['files'][i], container_class))
		}
		$(mail_view).find('.mail-info').append(files_container)
	}
	let mail_detail_view = buildMailView(mail) // Получение детального view

	mail_view.onclick = function(){ // Связь между view и детальным view письма
		mail_detail_view.style.display = 'block';
		$("body").css("overflow", "hidden");
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
			$(file_div).append($(generateMailFile(mail['files'][i], 'file')).append(
				$(`<div class="file-btns"><button onclick="window.open('${mail['files'][i]['url']}')" class="download-file" type="button"></button></div>`)[0]
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
	return $(`
		<div class="item ${mail_type}" data-aos="fade-up">
			<div class="mail-sender">
				<img src='${mail["sender"]["image"]}'/>
				<h4>${mail['sender']['surname']}<br>${mail['sender']['name']}</h4>
			</div>
			<div class="mail-info">
				<div class='item-header'>
					<h2>${mail['title']}</h2>
					<h3>${mail['date']}</h3>
				</div>
				<p class='item-text'>${mail['text']}</p>
			</div>
		</div>`)[0]
}

// Генерация подробного view письма
function generateMailDetailView(mail){
	return $(`
		<div class='form'>
			<div class="form-wrapper">
				<form>
					<div class='item-header'>
						<div class="user">
							<img src='${mail["sender"]["image"]}'/>
							<div class="info">
								<h4>${mail['sender']['permission']}</h4>
			  					<h2>${mail['sender']['surname']} ${mail['sender']['name'][0]}. ${mail['sender']['patronymic'][0]}.</h2>
			  				</div>
			  			</div>
			  			<nav style='display: flex; gap: 4px'>
			  				<button class='form-btn' type='button'><svg viewBox="0 0 24 24"><path d="M15,7H10.17V5.414A2,2,0,0,0,6.756,4L.876,9.879a3,3,0,0,0,0,4.242L6.756,20a2,2,0,0,0,3.414-1.414V17H16a6.006,6.006,0,0,1,6,6,1,1,0,0,0,2,0V16A9.01,9.01,0,0,0,15,7Z"/></svg></button>
			  				<button class='form-btn' type='button' onclick='updateImportantStatus(${mail.id})'><svg viewBox="0 0 24 24"><path d="M23.836,8.794a3.179,3.179,0,0,0-3.067-2.226H16.4L15.073,2.432a3.227,3.227,0,0,0-6.146,0L7.6,6.568H3.231a3.227,3.227,0,0,0-1.9,5.832L4.887,15,3.535,19.187A3.178,3.178,0,0,0,4.719,22.8a3.177,3.177,0,0,0,3.8-.019L12,20.219l3.482,2.559a3.227,3.227,0,0,0,4.983-3.591L19.113,15l3.56-2.6A3.177,3.177,0,0,0,23.836,8.794Zm-2.343,1.991-4.144,3.029a1,1,0,0,0-.362,1.116L18.562,19.8a1.227,1.227,0,0,1-1.895,1.365l-4.075-3a1,1,0,0,0-1.184,0l-4.075,3a1.227,1.227,0,0,1-1.9-1.365L7.013,14.93a1,1,0,0,0-.362-1.116L2.507,10.785a1.227,1.227,0,0,1,.724-2.217h5.1a1,1,0,0,0,.952-.694l1.55-4.831a1.227,1.227,0,0,1,2.336,0l1.55,4.831a1,1,0,0,0,.952.694h5.1a1.227,1.227,0,0,1,.724,2.217Z"/></svg></button>
			  				<button class='form-btn' type='button'><svg viewBox="0 0 24 24"><path d="M21,4H17.9A5.009,5.009,0,0,0,13,0H11A5.009,5.009,0,0,0,6.1,4H3A1,1,0,0,0,3,6H4V19a5.006,5.006,0,0,0,5,5h6a5.006,5.006,0,0,0,5-5V6h1a1,1,0,0,0,0-2ZM11,17a1,1,0,0,1-2,0V11a1,1,0,0,1,2,0Zm4,0a1,1,0,0,1-2,0V11a1,1,0,0,1,2,0ZM8.171,4A3.006,3.006,0,0,1,11,2h2a3.006,3.006,0,0,1,2.829,2Z"/></svg></button>
			  			</nav>
			  		</div>
			  		<hr class="divider"/>
			  		<h2>${mail['title']}</h2>
			  		<p class='item-text'>${mail['text']}</p>
			  		<div class='date__container'>
			  			<h5>${mail['date']}</h5>
			  		</div>
				</form>
			</div>
		</div>`)[0]
}

// Генерация файлов письма
function generateMailFile(file, class_name){
	return $(`
		<div class="${class_name}">
			<div class="file-info">
				<i class="file-${file['name'].split('.')[file['name'].split('.').length - 1]}"></i>
				<h4>${file['name']}</h4>
			</div>
		</div>`)[0]
}

// Генерация файлов в форме
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
