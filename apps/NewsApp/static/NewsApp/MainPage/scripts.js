let page = 0;
let file_array = Array()
let news_preview = undefined

// Закрытие формы
function close_form(bg) {
	bg.parentElement.style.display = 'none';
	$("body").css("position", "relative");
}

// Открытие формы по нажатию на курс
$("#widgets .item").click(function(event){
	$('#widgets .item').each(function(i, item){
		if(item == event.target.parentElement || item == event.target){
			$('#widgets .form')[i].style.display = 'block';
			$("body").css("position", "fixed");
		}
	})
});

// Добавление файлов по кнопке
$('#file-button').on('click', function(){
	$('#file-input')[0].value = '';
	$('#file-input').click();
});

// Добавление картинки по кнопке
$('#news-preview').on('click', function(){
	$('#preview-input')[0].value = ''
	$('#preview-input').click()
});

// Открытие формы создания новости
function open_add_news_form() {
	$('#news #add-news-form')[0].style.display = 'block';
	$("body").css("position", "fixed");
}

function addFileWidget(file){
	let file_div = document.createElement('div')
	file_div.className = 'file'

	let file_info = document.createElement('div')
	file_info.className = 'file-info'

	let file_icon = document.createElement('i')
	splited_name = file.name.split('.')
	file_icon.className = 'file-' + splited_name[splited_name.length - 1]

	let file_name = document.createElement('h4')
	file_name.innerHTML = file.name

	file_info.appendChild(file_icon)
	file_info.appendChild(file_name)

	let file_btns = document.createElement('div')
	file_btns.className = 'file-btns'

	let delete_btn = document.createElement('button')
	delete_btn.className = 'del-file'
	delete_btn.type = 'button'

	file_btns.appendChild(delete_btn)

	file_div.appendChild(file_info)
	file_div.appendChild(file_btns)

	return file_div
}

function addNewFile(event){
	if(event.target.files[0] != undefined){
		let file = event.target.files[0]
		file_array.push(file)
		let file_id = file_array.length - 1

		let container = $('#file-container')[0]
		let file_widget = addFileWidget(file)

		file_widget.childNodes[1].childNodes[0].onclick = function(click) {
			file_array.splice(file_id, 1)
			container.removeChild(file_widget)
		}
		
		container.appendChild(file_widget)
	}
}

function addNewsPreview(event){
	if(event.target.files[0] != undefined){
		$('#news-preview')[0].style.display = 'none'
		news_preview = event.target.files[0]

		let btns_container = $('#news-form-btns')[0]

		let preview_widget = addFileWidget(news_preview)
		preview_widget.childNodes[1].childNodes[0].onclick = function(click) {
			news_preview = undefined
			btns_container.removeChild(preview_widget)
			$('#news-preview')[0].style.display = 'block'
		}

		btns_container.insertBefore(preview_widget, btns_container.firstChild)
	}
}

function buildNews(news){
	let news_div = document.createElement('div');
	news_div.className = 'item';

	news_url = '/news/' + user_id + '/detail/' + news['id'];
	news_div.onclick = function(){
		location.href = location.origin + news_url;
	}

	let news_image = document.createElement('img');
	news_image.src = news['image'];

	let news_title = document.createElement('h2');
	news_title.innerHTML = news['title'];

	let news_text = document.createElement('p');
	news_text.innerHTML = news['content'];

	news_div.appendChild(news_image);
	news_div.appendChild(news_title);
	news_div.appendChild(news_text);

	return news_div
}

function getNewNews(){
	$.ajax({
		type: 'POST',
		url: send_news,
		data: {
			page: page,
			csrfmiddlewaretoken: csrf_token,
		},
		cache: false,
		success: function(response){
			for(let i in response['news']){
				$('#news-block')[0].appendChild(buildNews(response['news'][i]))
			}
		}
	})
	page++
}


$('#news-upload').on('click', function(){
	let news_form = new FormData();

	news_form.append('image', news_preview)
	for(let i = 0; i < file_array.length; i++){
		news_form.append('files', file_array[i])
	}

	news_form.append('title', $('#news-title')[0].value)
	news_form.append('content', $('#news-content')[0].value)
	news_form.append('csrfmiddlewaretoken', csrf_token)

	$.ajax({
		type: 'POST',
		url: create_news,
		data: news_form,
		cache: false,
		processData: false,
    	contentType: false,
		enctype: "multipart/form-data",
		success: function(response) { 
			location.href = response 
		}
	})
});