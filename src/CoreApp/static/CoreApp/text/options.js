var toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],
  [{ 'header': 1 }, { 'header': 2 }],
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'indent': '-1'}, { 'indent': '+1' }],
  ['link']
  ];

function initQuill(editor_id){

  new Quill(editor_id, {
    modules: {
      syntax: false,
      toolbar: toolbarOptions,
    },
    theme: 'snow',
    spellcheck: true,
    placeholder: 'Сообщение'
  });
}

initQuill('#editor')
