// Переход по вкладкам
function switch_to(section_id, btn) {
    for(let i = 0; i<4; i++){
        $('body > section')[i].style.display = 'none';
        $('aside button').removeClass('active');
    }
    document.getElementById(section_id).style.display = 'block';
    btn.className += ' active';
}

// Перезагрузка старницы с анимацией логотипа
function reload(logo){
    logo.style.animation = 'you_spin_me_right_round 1s';
    setTimeout("location.reload()", 800);
}

// Закрытие формы
function close_form(bg){
    bg.parentElement.style.display = 'none';
}

// Открытие формы по нажатию на урок
$("#diary .item").click(function(){
    $('#diary .form')[0].style.display = 'block';
});

// Открытие формы по нажатию на письмо
$("#mail .item").click(function(){
    $('#mail .form')[0].style.display = 'block';
});

// Открытие формы по нажатию на новость
$("#news .item").click(function(){
    $('#news .form')[0].style.display = 'block';
});

// Открытие формы создания письма
function open_create_mail_form(){
    $('#mail .form')[1].style.display = 'block';
}

// Поиск получателя
function filterFunction(input) {
	input.nextElementSibling.style.display = 'block';
	var filter = input.value.toUpperCase();
	var drops = input.nextElementSibling;
	var a = drops.getElementsByTagName("a");
	for (var i = 0; i < a.length; i++) {
		txtValue = a[i].textContent || a[i].innerText;
		if (txtValue.toUpperCase().indexOf(filter) > -1) {
			a[i].style.display = "block";
		} else {
			a[i].style.display = "none";
		}
	}
}

// Выбор получателя
function search_fill(a) {
	var input = a.parentElement.previousElementSibling;
	input.value = a.textContent;
	a.parentElement.style.display = 'none';
}