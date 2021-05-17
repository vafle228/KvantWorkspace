// Перезагрузка старницы с анимацией логотипа
function reload(logo) {
	logo.style.animation = 'you_spin_me_right_round 1s';
	setTimeout("location.reload()", 800);
}

// Сменить тему
function switch_theme(){
	if($('body').hasClass('light__theme')){
		themeChange('dark', user_color); user_theme = 'dark';
		$('.light__theme').toggleClass('light__theme dark__theme');
	} else {
		themeChange('light', user_color); user_theme = 'light';
		$('.dark__theme').toggleClass('dark__theme light__theme');
	}
}

// Сменить цветовую гамму
function switch_color_scheme(){
	if($('body').hasClass('blue__color__scheme')){
		themeChange(user_theme, 'orange'); user_color = 'orange';
		$('.blue__color__scheme').toggleClass('blue__color__scheme orange__color__scheme');
	} else {
		themeChange(user_theme, 'blue'); user_color = 'blue';
		$('.orange__color__scheme').toggleClass('orange__color__scheme blue__color__scheme');
	}
}

function themeChange(theme, color){
	$.ajax({
		type: 'POST',
		url: change_theme,
		data: {
			theme: theme,
			color: color,
			csrfmiddlewaretoken: csrf_token
		},
		cache: false
	})
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}