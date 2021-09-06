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

// Открыть меню
function open_menu(menu_id) {
	$(menu_id).show();
}

// Сменить тему
function switch_theme(){
	if($('body').hasClass('light__theme')){
		themeChange('dark', getColorScheme());
		$('.light__theme').toggleClass('light__theme dark__theme');
	} else {
		themeChange('light', getColorScheme());
		$('.dark__theme').toggleClass('dark__theme light__theme');
	}
}

// Сменить цветовую гамму
function switch_color_scheme(){
	let schemes = ['colorScheme__green', 'colorScheme__blue', 'colorScheme__red'];
	let scheme_name = ["green", "blue", "red"]; 
	
	let currentSchemeIndex = schemes.indexOf($('body').attr("colorScheme"));
	let nextSchemeIndex = (currentSchemeIndex + 1) % schemes.length;

	themeChange(getUserTheme(), scheme_name[nextSchemeIndex]);
	$('body').attr("colorScheme", schemes[nextSchemeIndex]);
}

// Сменить цветовую схему
function getColorScheme() {
	let schemes = ['colorScheme__green', 'colorScheme__blue', 'colorScheme__red'];
	let scheme_name = ["green", "blue", "pink"];
	
	let currentSchemeIndex = schemes.indexOf($('body').attr("colorScheme"));
	return scheme_name[currentSchemeIndex];
}

function getUserTheme(){
	return $('body').hasClass('light__theme') ? 'light' : 'dark'
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