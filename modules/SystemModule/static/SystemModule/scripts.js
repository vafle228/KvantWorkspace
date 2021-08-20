// Адаптивность от бога 2.0
$(window).resize(function(){
	$('body')[0].style.zoom = window.innerWidth / 1920 < 0.5 ? 0.5 : window.innerWidth / 1920;
});

// Открыть меню
function open_menu(menu_id) {
	$(menu_id).show();
}

// Сменить тему
function switch_theme(){
	if($('body').hasClass('light__theme')){
		themeChange('dark', getUserColorTheme());
		$('.light__theme').toggleClass('light__theme dark__theme');
	} else {
		themeChange('light', getUserColorTheme());
		$('.dark__theme').toggleClass('dark__theme light__theme');
	}
}

// Сменить цветовую гамму
function switch_color_scheme(){
	if($('body').hasClass('blue__color__scheme')){
		themeChange(getUserTheme(), 'orange');
		$('.blue__color__scheme').toggleClass('blue__color__scheme orange__color__scheme');
	} else {
		themeChange(getUserTheme(), 'blue');
		$('.orange__color__scheme').toggleClass('orange__color__scheme blue__color__scheme');
	}
}

function getUserColorTheme(){
	return $('body').hasClass('blue__color__scheme') ? 'blue' : 'orange'
}

function getUserTheme(){
	return $('body').hasClass('light__theme') ? 'light' : 'dark'
}

function themeChange(theme, color){
	$.ajax({
		type: 'POST',
		url: change_theme,
		data: {
			theme: theme,
			color: color,
			csrfmiddlewaretoken: getCookie('csrftoken')
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