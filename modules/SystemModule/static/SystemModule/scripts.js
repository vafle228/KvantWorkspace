// Перезагрузка старницы с анимацией логотипа
function reload(logo) {
	logo.style.animation = 'you_spin_me_right_round 1s';
	setTimeout("location.reload()", 800);
}

// Сменить тему
function switch_theme(){
	if($('body').hasClass('light__theme')){
		$('.light__theme').toggleClass('light__theme dark__theme');
	} else {
		$('.dark__theme').toggleClass('dark__theme light__theme');
	}
}

// Сменить цветовую гамму
function switch_color_scheme(){
	if($('body').hasClass('blue__color__scheme')){
		$('.blue__color__scheme').toggleClass('blue__color__scheme orange__color__scheme');
	} else {
		$('.orange__color__scheme').toggleClass('orange__color__scheme blue__color__scheme');
	}
}