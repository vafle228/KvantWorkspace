let file_array = Array();
let project_preview = undefined;


function addProjectPreviewHandler(event){
	if(event.target.files[0] !== undefined){
		project_preview = event.target.files[0]
		addProjectPreview(event.target.files[0])
	}
}

function addProjectFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array, "#file-container");
	}
}


// Генерация интерфейся превью
function addProjectPreview(project_preview){
	$('#project_preview')[0].style.display = 'none' // Скрытие кнопки "Загрузить картинку"

	let btns_container = $('#formButtons')[0] // Определение контейнера
	let preview_widget = addFileWidget(project_preview) // Получение html-а превью

	// Фунция по клику на "крестик"
	$(preview_widget).find('#del-btn')[0].onclick = function(click) {
		project_preview = undefined  // Забываем превью
		btns_container.removeChild(preview_widget) // Чистим html от превью
		$('#project_preview')[0].style.display = 'flex' // Открываем кнопку
	}
	btns_container.insertBefore(preview_widget, btns_container.firstElementChild.nextSibling) // Добавление превью
}

// Поиск пользователя
function filterFunction(input, select) {
	let substr = input.value.toUpperCase();
	if (substr.trim()) {
		$(select).show();
		let users = $(select).find('.userSelect__user');

		// Сортируем
		users.sort((a, b) => {
			a = $(a).find('h3')[0].textContent.toUpperCase().indexOf(substr);
			b = $(b).find('h3')[0].textContent.toUpperCase().indexOf(substr);

			if (a == -1) return 1
			if (b == -1) return -1
			return a - b
		});

		// Перезаполняем
		$(select).find('.userSelect__user').detach();
		users.map(index => $(select).append(users[index]));
		
		// Скрываем пользователей неудолетворяющих поиску
		users.map(
			(index) => $(users[index]).find('h3')[0].textContent.toUpperCase().indexOf(substr) !== -1 ? $(users[index]).show() : $(users[index]).hide()
		);
	}
	else { $(select).hide(); }
}