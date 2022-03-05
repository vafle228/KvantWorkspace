
function page_adaptation(){

	let ratio = window.innerWidth / 2160 < 0.75 ? 0.75 : window.innerWidth / 2160;

	$("body").css({
		"zoom": ratio,
		"-moz-zoom": ratio,
		"width": `${ 1 / ratio * 100}vw`,
		"height": `${ 1 / ratio * 100}vh`
	});
}

$(window).ready(() => page_adaptation());

$(window).resize(() => page_adaptation());


// Закрытие форм при клике вне
$(document).mouseup(function (e) {
	let exceptions = [$(".form-wrapper"), $(".alert"), $(".trigger"), $(".modal__viewport")]

	if(!(exceptions.filter(exception => exception.has(e.target).length !== 0).length)){
		$(".form").removeClass("active");
		$(".mainContainer").css("overflow-y", "scroll");
		$(".userSelect").hide();
		$("menu").removeClass("active");
		$(".list").hide();
		$(".modal").removeClass("active");
	}
});

// Горячие клавиши
$('body').keyup((event) => {
	if (event.keyCode == 27){
		$(".form").removeClass("active");
		$(".modal").removeClass("active");
		$(".mainContainer").css("overflow-y", "scroll");
	} 
});

// Открыть форму по ID
function open_form(form_id) {
	$(".mainContainer").css("overflow", "hidden");
	$(form_id).addClass("active");
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
		users.map(
			(index) => $(users[index]).find('h3')[0].textContent.toUpperCase().indexOf(substr) !== -1 ? $(users[index]).show() : $(users[index]).hide()
		);
	}
	else { $('.userSelect').hide(); }
}

// Сменить тему оформления
function switch_theme() {
	$('body').toggleClass('light__theme dark__theme');
	page_adaptation();
}

// Сменить цветовую схему
function switch_color_scheme() {

	schemes = ['colorScheme__green', 'colorScheme__blue', 'colorScheme__red', 'colorScheme__purple'];

	let currentSchemeIndex = schemes.indexOf($('body').attr("colorScheme"));
	let nextSchemeIndex = (currentSchemeIndex + 1) % schemes.length;

	$('body').attr("colorScheme", schemes[nextSchemeIndex]);
	page_adaptation();
}


// Кнопка вернуться в начало страницы
arrowTop.onclick = function () {
	window.scrollTo(pageXOffset, 0);
};
window.addEventListener('scroll', function () {
	arrowTop.hidden = (pageYOffset < document.documentElement.clientHeight);
});


// Копирование текста
function copytext(el) {
    var $tmp = $("<textarea>");
    $("body").append($tmp);
    $tmp.val($(el).text()).select();
    document.execCommand("copy");
    
	let alert = $(`
		<div class='alert good'>
            <svg viewBox="0 0 448 512">
                <path opacity='0.6' d="M400 32H48A48 48 0 0 0 0 80v352a48 48 0 0 0 48 48h352a48 48 0 0 0 48-48V80a48 48 0 0 0-48-48zM224 384a32 32 0 1 1 32-32 32 32 0 0 1-32 32zm38.24-238.41l-12.8 128A16 16 0 0 1 233.52 288h-19a16 16 0 0 1-15.92-14.41l-12.8-128A16 16 0 0 1 201.68 128h44.64a16 16 0 0 1 15.92 17.59z"></path>
                <path d="M246.32 128h-44.64a16 16 0 0 0-15.92 17.59l12.8 128A16 16 0 0 0 214.48 288h19a16 16 0 0 0 15.92-14.41l12.8-128A16 16 0 0 0 246.32 128zM224 320a32 32 0 1 0 32 32 32 32 0 0 0-32-32z"></path>
            </svg>
            <p>Скопировано</p>
            <button onclick='$(this).parent().remove()'>×</button>
        </div>
	`);

	$tmp.remove();

	$('.alertsContainer').append(alert);
	setTimeout(() => {
		alert.fadeOut();
		setTimeout(() => {
			alert.detach();
		}, 1000);
	}, 1000)
	
}