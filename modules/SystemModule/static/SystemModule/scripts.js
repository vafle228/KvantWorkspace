function page_adaptation(){

	let ratio = window.innerWidth / 1920 < 0.75 ? 0.75 : window.innerWidth / 1920;

	$("body").css({
		"zoom": ratio,
		"-moz-zoom": ratio,
		"width": `${ 1 / ratio * 100}vw`,
		"height": `${ 1 / ratio * 100}vh`,
	});
}

$(window).ready(() => page_adaptation());

$(window).resize(() => page_adaptation());

$(document).mouseup(function (e) {
	let exceptions = [$(".form-wrapper"), $(".alert"), $(".trigger")]

	if(!(exceptions.filter(exception => exception.has(e.target).length !== 0).length)){
		$(".form").removeClass("active");
		$("body").css("overflow-y", "scroll");
		$(".userSelect").hide();
		$("menu").removeClass("active");
	}
});

// Сменить тему
function switch_theme(){
	$('body').toggleClass('light__theme dark__theme');
	themeChange(getUserTheme(), getColorScheme());
}

// Сменить цветовую гамму
function switch_color_scheme(){
	let schemes = [
		'colorScheme__green', 'colorScheme__blue', 
		'colorScheme__red', 'colorScheme__purple'
	];
	
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
		case "colorScheme__purple": return "purple"
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
		<div class='alert' data-aos="fade-up">
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
			else{
				if(response.link != "Reload"){ location.href = response.link }
				else{ location.reload() }
			}
		}
	})
}

function updateGetUrlParams(param, value){
	let current_href = new URL(location.href)
	current_href.searchParams.set(param, value)

	return current_href.toString()
}

// <=== Генерация файлового превью ===>

// Генерация интерфейса файла
function addNewFile(file, array, container_id){
	let container = $(container_id)[0] // init контейнера
	let file_widget = addFileWidget(file) // Получение html view

	// Функция по клику на "крестик"
	$(file_widget).find('#del-btn')[0].onclick = function(click) {
		for(let i = 0; i < array.length; i++){
			if(array[i] == file){ array.splice(i, 1) }
		} 
		container.removeChild(file_widget) // Уборка html view
	}
	
	container.appendChild(file_widget) // Добавление view в контейнер
	
}

function getFileSize(nbytes){
	let suffix_index = 0
    let suffixes = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
    
    while(nbytes >= 1024 && suffix_index < suffixes.length - 1){
		nbytes /= 1024.
        suffix_index += 1
	}
	console.log(nbytes)
    size = nbytes.toFixed(2).split(".00")[0]

    return `${size} ${suffixes[suffix_index]}`
}

// Генерация файлов в форме
function addFileWidget(file){
	return $(`
		<div class='file'>
			<i class='file-${file.name.split('.')[file.name.split('.').length - 1]}'></i>
			<div class="file__info">
				<h4 class='file__name'>${file.name}</h4>
				<p class="file__size">${getFileSize(parseFloat(file.size))}</p>
			</div>
			<div class="file__actions">
				<button type='button' id='del-btn'>
					<svg viewBox="0 0 448 512">
						<path opacity='0.3' d="M53.2 467L32 96h384l-21.2 371a48 48 0 0 1-47.9 45H101.1a48 48 0 0 1-47.9-45z"></path>
						<path d="M0 80V48a16 16 0 0 1 16-16h120l9.4-18.7A23.72 23.72 0 0 1 166.8 0h114.3a24 24 0 0 1 21.5 13.3L312 32h120a16 16 0 0 1 16 16v32a16 16 0 0 1-16 16H16A16 16 0 0 1 0 80z"></path>
					</svg>
				</button>
			</div>
		</div>`)[0]
}
