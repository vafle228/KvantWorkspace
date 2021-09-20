let page = 1;
let users = Array();
let file_array = Array();

function openFileDialog(fileInput){
	$(fileInput)[0].value = '';
	$(fileInput)[0].click();
}

// <=== Костыли Вадима ===>
function updateFormCondition(btn){
	$("#newMailItemForm").toggleClass('fullscreen');

	if ($("#newMailItemForm").hasClass("fullscreen")){
		$(btn).html(`
			<svg viewBox="0 0 448 512"><path opacity='0.6' d="M224 280v112c0 21.38-25.8 32.09-40.92 17L152 376l-99.31 99.31a16 16 0 0 1-22.63 0L4.69 449.94a16 16 0 0 1 0-22.63L104 328l-32.92-31c-15.12-15.12-4.41-41 17-41h112A24 24 0 0 1 224 280z">
			</path><path d="M443.31 62.06a16 16 0 0 1 0 22.63L344 184l32.92 31c15.12 15.12 4.41 41-17 41H248a24 24 0 0 1-24-24V120c0-21.38 25.8-32.09 40.92-17L296 136l99.31-99.31a16 16 0 0 1 22.63 0z"></path></svg>
		`);
	} else {
		$(btn).html(`
			<svg viewBox="0 0 448 512"><path opacity='0.6' d="M0 456V344c0-21.38 25.8-32.09 40.92-17L72 360l92.69-92.69a16 16 0 0 1 22.62 0l25.38 25.38a16 16 0 0 1 0 22.62L120 408l32.92 31c15.12 15.12 4.41 41-17 41H24a24 24 0 0 1-24-24z"></path>
			<path d="M235.31 196.69L328 104l-32.92-31c-15.12-15.12-4.41-41 17-41h112A24 24 0 0 1 448 56v112c0 21.38-25.8 32.09-40.92 17L376 152l-92.69 92.69a16 16 0 0 1-22.62 0l-25.38-25.38a16 16 0 0 1 0-22.62z"></path></svg>
		`);
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

// <=== Работа с файлами ===>

function addMailFileHandler(event){
	for(let i = 0; i < event.target.files.length; i++){
		file_array.push(event.target.files[i])
		addNewFile(event.target.files[i], file_array, "#file-container");
	}
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
		
		// Скрываем пользователей неудолетворяющих поиску
		users.map((index) => $(users[index]).find('h3')[0].textContent.toUpperCase().indexOf(substr) !== -1 ? $(users[index]).show() : $(users[index]).hide());
	}
	else { $('.userSelect').hide(); }
}
