// Перезагрузка старницы с анимацией логотипа
function reload(logo) {
	logo.style.animation = 'you_spin_me_right_round 1s';
	setTimeout("location.reload()", 800);
}

// Закрытие форм и меню при клике вне
$(document).mouseup(function (e) {
	var container = $(".form-wrapper");
	if (container.has(e.target).length === 0 && $('#settings').has(e.target).length === 0) {
		$(".form").hide();
		$("menu").hide();
		$("body").css("overflow-y", "scroll");
	}
});

// Открыть меню
function open_menu(menu_id) {
	$(menu_id).show();
}

// Открыть форму
function open_form(form_id) {
	$(form_id).show();
	$("body").css("overflow", "hidden");
}

// Открытие формы по нажатию на урок
$("#diary .item").click(function () {
	$('#diary .form')[0].style.display = 'block';
	$("body").css("overflow", "hidden");
});

// Открытие формы по нажатию на курс
$("#widgets .item").click(function () {
	$('#widgets .form')[0].style.display = 'block';
	$("body").css("overflow", "hidden");
});

// Открытие формы по нажатию на письмо
$("#mail .item").click(function () {
	$('#mail .form')[0].style.display = 'block';
	$("body").css("overflow", "hidden");
});


let filters = ['Ученик', 'Ученик', 'Группа', 'Администратор'];
// Поиск пользователя
function filterFunction(input) {
	let substr = input.value.toUpperCase();
	if (substr.trim()) {
		$('.unselected').show();
		let users = $('.unselected .user').map(function (index) {
			let user = $('.unselected .user')[index]

			user.style.display = 'none';
			return user
		});

		let unblocked = users.map(function (index) {
			let user = users[index]

			let name = $(user).find('h2')[0].textContent;
			let category = $(user).find('h4')[0].textContent;

			if (name.toUpperCase().indexOf(substr) !== -1 && filters.indexOf(category) !== -1) {
				user.style.display = 'flex'
				return user
			}
		})

		if (unblocked.length) { $('.unselected').show() }
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

// Сменить тему
function switch_theme() {
	if ($('body').hasClass('light__theme')) {
		$('.light__theme').toggleClass('light__theme dark__theme');
	} else {
		$('.dark__theme').toggleClass('dark__theme light__theme');
	}
}

// Сменить цветовую гамму
function switch_color_scheme() {
	if ($('body').hasClass('blue__color__scheme')) {
		$('.blue__color__scheme').toggleClass('blue__color__scheme orange__color__scheme');
	} else {
		$('.orange__color__scheme').toggleClass('orange__color__scheme blue__color__scheme');
	}
}