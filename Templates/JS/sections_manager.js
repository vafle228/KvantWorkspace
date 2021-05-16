// Перезагрузка старницы с анимацией логотипа
function reload(logo) {
	logo.style.animation = 'you_spin_me_right_round 1s';
	setTimeout("location.reload()", 800);
}

// Закрыть форму
$(document).mouseup(function (e) {
	var container = $("form");
	if (container.has(e.target).length === 0) {
		$(".form").hide();
	}
});

// Открыть форму
function open_form(form_class) {
	$(form_class).show();
}

// Открытие формы по нажатию на урок
$("#diary .item").click(function () {
	$('#diary .form')[0].style.display = 'block';
	$("body").css("position", "fixed");
});

// Открытие формы по нажатию на курс
$("#widgets .item").click(function () {
	$('#widgets .form')[0].style.display = 'block';
	$("body").css("position", "fixed");
});

// Открытие формы по нажатию на письмо
$("#mail .item").click(function () {
	$('#mail .form')[0].style.display = 'block';
	$("body").css("position", "fixed");
});

// Открытие форму создания новости
function open_add_news_form() {
	$('#news #add-news-form')[0].style.display = 'block';
	$("body").css("position", "fixed");
}

// Открытие формы создания письма
function open_create_mail_form() {
	$('#mail .form')[1].style.display = 'block';
	$("body").css("position", "fixed");
}


let filters = [];
// Поиск пользователя
function filterFunction(input) {
	var substr = input.value.toUpperCase();
	if (substr.trim()) {
		$('.unselected').show();
		var users = $('.unselected .user');
		var counter = 0;
		for (var i = 0; i < users.length; i++) {
			users[i].style.display = 'none';

			name_ = users[i].getElementsByTagName('h2')[0].textContent;
			category_ = users[i].getElementsByTagName('h4')[0].textContent;
			if (name_.toUpperCase().indexOf(substr) > -1 && filters.indexOf(category_) !== -1) {
				users[i].style.display = 'flex';
				counter += 1;
			}
			if (!counter) {
				$('.unselected').hide();
			}
		}
	} else {
		$('.unselected').hide();
	}
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

// Выбор получателя письма
function search_fill(a) {
	var input = a.parentElement.previousElementSibling;
	input.value = a.textContent;
	a.parentElement.style.display = 'none';
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