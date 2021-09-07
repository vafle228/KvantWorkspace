
function page_adaptation(){

	let ratio = window.innerWidth / 1920 < 0.5 ? 0.5 : window.innerWidth / 1920;

	$("body").css({
		"zoom": ratio,
		"-moz-zoom": ratio,
		"width": `${ 1 / ratio * 100}vw`,
		// "height": `${ 1 / ratio * 100}%`
	});
}

$(window).ready(function () {
	page_adaptation();
});

$(window).resize(function () {
	page_adaptation();
});


// Закрытие форм при клике вне
$(document).mouseup(function (e) {
	let exceptions = [$(".form-wrapper"), $("menu"), $(".alert")]

	if(!(exceptions.filter(exception => exception.has(e.target).length !== 0).length)){
		$(".form").removeClass("active");
		$("body").css("overflow-y", "scroll");
		$(".userSelect").hide();
	}
});

// Открыть форму по ID
function open_form(form_id) {
	$("body").css("overflow", "hidden");
	$(form_id).addClass("active");
}


let filters = ['Ученик', 'Учитель', 'Группа', 'Администратор'];
// Поиск пользователя
function filterFunction(input) {
	let substr = input.value.toUpperCase();
	if (substr.trim()) {
		$('.userSelect').show();
		let users = $('.userSelect__user').map(function (index) {
			let user = $('.userSelect__user')[index]

			$(user).removeClass('active');
			return user
		});

		let unblocked = users.map(function (index) {
			let user = users[index]

			let name = $(user).find('h3')[0].textContent;
			let category = $(user).find('p')[0].textContent;

			if (name.toUpperCase().indexOf(substr) !== -1) {
				$(user).addClass('active');
				return user
			}
		})

		if (unblocked.length) { $('.userSelect').show() }
		else { $('.userSelect').hide(); }
	}
	else { $('.userSelect').hide(); }
}

// Применение фильтра
function filter_applying(button, filter) {

	if (filters.indexOf(filter) !== -1) {
		filters.splice(filters.indexOf(filter), 1);
	} else {
		filters.push(filter);
	}

	$(button).toggleClass("active", "inactive")
	filterFunction($('.dropdown-input')[0]);
}

// Сменить тему оформления
function switch_theme() {
	$('body').toggleClass('light__theme dark__theme');
}

// Сменить цветовую схему
function switch_color_scheme() {

	schemes = ['colorScheme__green', 'colorScheme__blue', 'colorScheme__red'];

	let currentSchemeIndex = schemes.indexOf($('body').attr("colorScheme"));
	let nextSchemeIndex = (currentSchemeIndex + 1) % schemes.length;

	$('body').attr("colorScheme", schemes[nextSchemeIndex]);
}


// Кнопка вернуться в начало страницы
arrowTop.onclick = function () {
	window.scrollTo(pageXOffset, 0);
};
window.addEventListener('scroll', function () {
	arrowTop.hidden = (pageYOffset < document.documentElement.clientHeight);
});