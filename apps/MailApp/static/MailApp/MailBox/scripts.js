let page = 1;
let users = Array();
let file_array = Array();

function openFileDialog(fileInput){
	$(fileInput)[0].value = '';
	$(fileInput)[0].click();
}

// <=== Костыли Вадима ===>

function closeForm(btn){
	$("#newMailItemForm").toggleClass('closed');
	
	if ($("#newMailItemForm").hasClass("closed")){
		
		$(btn).html(`<svg viewBox="0 0 512 512"><path opacity='0.6' d="M400 320h32a16 16 0 0 1 16 16v128a48 48 0 0 1-48 48H48a48 48 0 0 1-48-48V112a48 48 0 0 1 48-48h160a16 16 0 0 1 16 16v32a16 16 0 0 1-16 16H64v320h320V336a16 16 0 0 1 16-16z"></path><path d="M512 24v128c0 21.47-26 32-41 17l-35.71-35.71L191.8 376.77a24 24 0 0 1-33.94 0l-22.63-22.63a24 24 0 0 1 0-33.94L378.76 76.68 343.05 41C328 25.9 338.66 0 360 0h128a24 24 0 0 1 24 24z"></path></svg>`);
		
		$("#newMailItemForm").removeClass("expanded");
		
		if ($("#mailSubject").val()){
			$(btn).parent().find("h3").html($("#mailSubject").val());
		}
	} else {
		$(btn).html(`<svg viewBox="0 0 512 512" style="transform: scale(0.8);"><path d="M464 352H48c-26.5 0-48 21.5-48 48v32c0 26.5 21.5 48 48 48h416c26.5 0 48-21.5 48-48v-32c0-26.5-21.5-48-48-48z"></path></svg>`);
		
		$(btn).parent().find("h3").html("Новое сообщение");
	}
}

function expandForm(btn){
	$("#newMailItemForm").toggleClass('expanded');
   
	
	if ($("#newMailItemForm").hasClass("expanded")){
		$(btn).html(`<svg viewBox="0 0 448 512"><path opacity='0.6' d="M224 280v112c0 21.38-25.8 32.09-40.92 17L152 376l-99.31 99.31a16 16 0 0 1-22.63 0L4.69 449.94a16 16 0 0 1 0-22.63L104 328l-32.92-31c-15.12-15.12-4.41-41 17-41h112A24 24 0 0 1 224 280z"></path><path d="M443.31 62.06a16 16 0 0 1 0 22.63L344 184l32.92 31c15.12 15.12 4.41 41-17 41H248a24 24 0 0 1-24-24V120c0-21.38 25.8-32.09 40.92-17L296 136l99.31-99.31a16 16 0 0 1 22.63 0z"></path></svg>`);
		$("#newMailItemForm").removeClass("closed");
	} else {
		$(btn).html(`<svg viewBox="0 0 448 512"><path opacity='0.6' d="M0 456V344c0-21.38 25.8-32.09 40.92-17L72 360l92.69-92.69a16 16 0 0 1 22.62 0l25.38 25.38a16 16 0 0 1 0 22.62L120 408l32.92 31c15.12 15.12 4.41 41-17 41H24a24 24 0 0 1-24-24z"></path><path d="M235.31 196.69L328 104l-32.92-31c-15.12-15.12-4.41-41 17-41h112A24 24 0 0 1 448 56v112c0 21.38-25.8 32.09-40.92 17L376 152l-92.69 92.69a16 16 0 0 1-22.62 0l-25.38-25.38a16 16 0 0 1 0-22.62z"></path></svg>`);
	}
}

$('.userSelect__user').click( function() {
	
	if ($(this).parent().hasClass('userSelect')){
		$(this).detach();
		users.push($(this).attr('value'))
		$('#userSearch').before($(this));
	} else {
		$(this).detach();
		for(let i = 0; i < users.length; i++){
			if(users[i] == $(this).attr('value')) { users.splice(i, 1) }
		}
		$(this).appendTo($('.userSelect'));
	}

	$('#userSearch').val('');
	$('#userSearch').focus();
});

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
// <=== Работа с файлами ===>

function addMailFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array);
	}
}

// Генерация интерфейса файла
function addNewFile(file){
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

// Поиск пользователя
function filterFunction(input) {
	let substr = input.value.toUpperCase();
	if (substr.trim()) {
		$('.userSelect').show();
		let users = $('.userSelect .userSelect__user');

		// Сортируем
		users.sort((a, b) => {
			a = $(a).find('h3')[0].textContent.toUpperCase().indexOf(substr);
			b = $(b).find('h3')[0].textContent.toUpperCase().indexOf(substr);

			if (a == -1) return 1
			if (b == -1) return -1
			return a - b
		});

		// Перезаполняем
		$('.userSelect').find('.userSelect__user').detach();
		users.map(index => $('.userSelect').append(users[index]));

		users.map((index) => $(users[index]).find('h3')[0].textContent.toUpperCase().indexOf(substr) !== -1 ? $(users[index]).show() : $(users[index]).hide());
	}
	else { $('.userSelect').hide(); }
}
