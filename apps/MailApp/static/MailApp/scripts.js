let page = 0;

// Закрытие формы
function close_form(bg) {
	bg.parentElement.style.display = 'none';
	$("body").css("position", "relative");
}
// Открытие формы создания письма
function open_create_mail_form() {
	$('#mail .form')[0].style.display = 'block';
	$("body").css("position", "fixed");
}

// Поиск получателя письма
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

// Выбор получателя письма
function search_fill(a) {
	var input = a.parentElement.previousElementSibling;
	input.value = a.textContent;
	a.parentElement.style.display = 'none';
}

function getNewMails(){
	$.ajax({
		type: 'POST',
		url: send_mail,
		data: {
			page: page,
			csrfmiddlewaretoken: csrf_token,
		},
		cache: false,
		success: function(response){
			for(let i in response['mails']){
				buildNewMail(response['mails'][i]);
			}
		}
	})
	page++
	if(page * 8 >= max_mails){
		$('#more-mails')[0].style.display = 'none'
	}
}

function updateMailStatus(mail_id, mail){
	$.ajax({
		type: 'POST',
		url: change_status,
		data: {
			mail_id: mail_id,
			csrfmiddlewaretoken: csrf_token,
		},
		cache: false,
		success: function(response){
			mail.className = 'item old-mail';
		}
	})
}

function buildNewMail(mail){
	let mail_div = document.createElement('div');
	mail_div.className = 'item new-mail';
	if (mail['is_read']) { mail_div.className = 'item old-mail'; }

	[header_div, mail_content] = generateMail(mail, true)

	mail_div.appendChild(header_div); mail_div.appendChild(mail_content)

	if (mail['files'].length !== 0) {
		let files_div = document.createElement('div');
		files_div.className = 'files';
		files_div.style.width = '100%'

		for(let i in mail['files']){
			let file_div = generateMailFile(mail['files'][i])
			files_div.appendChild(file_div);
		}
		mail_div.appendChild(files_div)
	}
	let mail_view = buildMailView(mail)

	mail_div.onclick = function(){
		mail_view.style.display = 'block';
		$("body").css("position", "fixed");
		updateMailStatus(mail['id'], mail_div)
	}

	$('#mail_container')[0].appendChild(mail_div)
}

function buildMailView(mail){
	let div_form = document.createElement('div');
	div_form.className = 'form';

	let div_filter = document.createElement('div');
	div_filter.className = 'filter';
	div_filter.onclick = function(event) { 
		close_form(div_filter); 
	}

	let div_wrapper = document.createElement('div');
	div_wrapper.className = 'form-wrapper';

	let mail_view = document.createElement('form');

	[header_div, mail_content] = generateMail(mail, false)
	
	let date_div = generateMailDate(mail)

	mail_view.appendChild(header_div); 
	mail_view.appendChild(mail_content);
	mail_view.appendChild(date_div); 

	if(mail['files'].length !== 0){
		let dividing_line = document.createElement('hr');
		dividing_line.className = 'divider'
		mail_view.appendChild(dividing_line);
	}

	if (mail['files'].length !== 0) {
		let form_item = document.createElement('div')
		form_item.className = 'item-header';

		let files_div = document.createElement('div');
		files_div.className = 'files';
		files_div.style.width = '100%';

		for(let i in mail['files']){
			let file_div = generateMailFile(mail['files'][i])
			files_div.appendChild(file_div);
		}
		form_item.appendChild(files_div); mail_view.appendChild(form_item);
	}
	div_wrapper.appendChild(mail_view);
	div_form.appendChild(div_filter); 
	div_form.appendChild(div_wrapper);

	$('#mail')[0].appendChild(div_form)

	return div_form
}

function generateMail(mail, is_mail){
	let header_div = document.createElement('div');
	header_div.className = 'item-header';

	let title_div = document.createElement('div');
	title_div.className = 'lesson-title';

	let mail_title = document.createElement('h2');
	mail_title.innerHTML = mail['title'];

	title_div.appendChild(mail_title);

	if(is_mail){
		let mail_date = document.createElement('h3');
		mail_date.innerHTML = `${mail['date'].split('-')[2]}.${mail['date'].split('-')[1]} ${mail['date'].split('-')[0]}`;	
		title_div.appendChild(mail_date);
	}

	let sender_div = document.createElement('div');
	sender_div.className = 'lesson-teacher';

	let mail_sender = document.createElement('h4');
	mail_sender.innerHTML = mail['sender']['name'];

	let sender_image = document.createElement('img');
	sender_image.src = mail['sender']['image'];

	sender_div.appendChild(mail_sender); sender_div.appendChild(sender_image);

	header_div.appendChild(title_div); header_div.appendChild(sender_div);

	let mail_content = document.createElement('p');
	mail_content.className = 'item-text';
	mail_content.innerHTML = mail['text'];

	return [header_div, mail_content]
}

function generateMailFile(file){
	let file_div = document.createElement('div');
	file_div.className = 'file';
	
	let file_info = document.createElement('div');
	file_info.className = 'file-info';

	let file_icon = document.createElement('i');
	splited_name = file['name'].split('.');
	file_icon.className = 'file-' + splited_name[splited_name.length - 1];

	let file_name = document.createElement('h4');
	file_name.innerHTML = file['name'];

	file_info.appendChild(file_icon); file_info.appendChild(file_name);

	let file_btns = document.createElement('div');
	file_btns.className = 'file-btns';

	let download_btn = document.createElement('button');
	download_btn.className = 'download-file';
	download_btn.type = 'button';
	download_btn.onclick = function(){ window.open(file[i]['url']); }

	file_btns.appendChild(download_btn); 
	file_div.appendChild(file_info); file_div.appendChild(file_btns);

	return file_div
}

function generateMailDate(mail){
	let date_div = document.createElement('div');

	let date_span = document.createElement('span');
	date_span.className = 'fi-rr-calendar';
	date_span.style.fontSize = '0.8rem';
	date_span.style.marginRight = '5px';

	let date = `${mail['date'].split('-')[2]}.${mail['date'].split('-')[1]} ${mail['date'].split('-')[0]}`;

	let date_text = document.createElement('h3');
	date_text.style.display = 'inline-block';
	date_text.innerHTML = `Дата отправки ${date}`;

	date_div.appendChild(date_span); date_div.appendChild(date_text);

	return date_div
}
