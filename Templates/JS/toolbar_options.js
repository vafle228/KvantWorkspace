var toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],
  // ['blockquote', 'code-block'],
  [{ 'header': 1 }, { 'header': 2 }],
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'indent': '-1'}, { 'indent': '+1' }],
  // [{ 'color': [] }, { 'background': [] }],
  // [{ 'align': [] }],
  // ['formula'],
  ['link']
];

var quill = new Quill('#editor', {
  modules: {
    toolbar: toolbarOptions,
  },
  theme: 'snow',
});

var quill = new Quill('#editor1', {
  modules: {
    toolbar: toolbarOptions,
  },
  theme: 'snow',
});

var quill = new Quill('#editor2', {
  modules: {
    toolbar: toolbarOptions,
  },
  theme: 'snow',
});