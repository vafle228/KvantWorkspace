// Поиск пользователя
function filterFunction(input, select, option, parameter, hide) {
	let substr = input.value.toUpperCase();
	if (substr.trim()) {
		$(select).show();
		let users = $(select).find(option);

		// Сортируем
		users.sort((a, b) => {
			a = $(a).find(parameter)[0].textContent.toUpperCase().indexOf(substr);
			b = $(b).find(parameter)[0].textContent.toUpperCase().indexOf(substr);

			if (a == -1) return 1
			if (b == -1) return -1
			return a - b
		});

		// Перезаполняем
		$(select).find(option).detach();
		users.map(index => $(select).append(users[index]));
		
		// Скрываем пользователей неудолетворяющих поиску
		users.map((index) => 
			$(users[index]).find(parameter)[0].textContent.toUpperCase().indexOf(substr) !== -1 ? $(users[index]).show() : $(users[index]).hide()
		);
	}
	else {
		hide ? $(select).hide() : $(select).find(option).show();
	}

	// Специально для SearchPage
	resetCheckboxes();
}

function filterApplying(substr, select, option, parameter){
	let users = $(select).find(option);
	users.map((index) => {
		let flag = false
		$(users[index]).find(parameter).toArray().forEach(element => {
			if (element.textContent.indexOf(substr) !== -1)
				flag = true
		});
		flag ? $(users[index]).show() : $(users[index]).hide();
	});

	// Специально для SearchPage
	resetCheckboxes();
}

function selectAll(mainChecbox){
    $('.tableRow').toArray().forEach((tableRow) => {
        if ($(tableRow).css('display') !== 'none')
            $(tableRow).find('input[type=checkbox]').prop('checked', $(mainChecbox).prop('checked'))
    });
}
function resetCheckboxes(){
    $('input[type=checkbox]').prop('checked', false);
}