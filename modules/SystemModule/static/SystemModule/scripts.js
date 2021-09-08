function page_adaptation(){

	let ratio = window.innerWidth / 1920 < 0.5 ? 0.5 : window.innerWidth / 1920;

	$("body").css({
		"zoom": ratio,
		"-moz-zoom": ratio,
		"width": `${ 1 / ratio * 100}vw`,
	});
}

$(window).ready(() => page_adaptation());

$(window).resize(() => page_adaptation());

// Сменить тему
function switch_theme(){
	$('body').toggleClass('light__theme dark__theme');
	themeChange(getUserTheme(), getColorScheme());
}

// Сменить цветовую гамму
function switch_color_scheme(){
	let schemes = ['colorScheme__green', 'colorScheme__blue', 'colorScheme__red'];
	
	let currentSchemeIndex = schemes.indexOf($('body').attr("colorScheme"));
	let nextSchemeIndex = (currentSchemeIndex + 1) % schemes.length;

	$('body').attr("colorScheme", schemes[nextSchemeIndex]);
	themeChange(getUserTheme(), getColorScheme());
}

// Получить текущую схему
function getColorScheme() {
	switch($("body").attr("colorScheme")){
		case "colorScheme__green": return "green";
		case "colorScheme__blue": return "blue";
		case "colorScheme__red": return "red";
		default: return "blue";
	}
	
}

function getUserTheme(){
	return $('body').hasClass('light__theme') ? 'light' : 'dark'
}

// <=== Общие приколы ===>
function errorAlert(errorsObj){
	
	function _errorAlert(message){
		$("#alertsContainer").append(`
		<div class='alert' data-aos="fade-left">
			<svg viewBox="0 0 448 512">
				<path opacity='0.6' d="M400 32H48A48 48 0 0 0 0 80v352a48 48 0 0 0 48 48h352a48 48 0 0 0 48-48V80a48 48 0 0 0-48-48zM224 384a32 32 0 1 1 32-32 32 32 0 0 1-32 32zm38.24-238.41l-12.8 128A16 16 0 0 1 233.52 288h-19a16 16 0 0 1-15.92-14.41l-12.8-128A16 16 0 0 1 201.68 128h44.64a16 16 0 0 1 15.92 17.59z"></path>
				<path d="M246.32 128h-44.64a16 16 0 0 0-15.92 17.59l12.8 128A16 16 0 0 0 214.48 288h19a16 16 0 0 0 15.92-14.41l12.8-128A16 16 0 0 0 246.32 128zM224 320a32 32 0 1 0 32 32 32 32 0 0 0-32-32z"></path>
			</svg>
			<p>${message}</p>
			<button onclick='$(this).parent().remove()'>×</button>
		</div>
		`)
	}

	for(let error in errorsObj){
		errorsObj[error].forEach(element => _errorAlert(element))
	}
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

function sendInstanceData(form, post_url){
	$.ajax({
		type: 'POST',
		url: post_url,
		data: form,
		cache: false,
		processData: false,
		contentType: false,
		enctype: "multipart/form-data",
		success: function(response) {
			if(response.status == 400){ errorAlert(response.errors) }
			else{ location.href = response.link }
		}
	})
}