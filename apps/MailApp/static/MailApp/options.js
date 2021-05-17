// Редактирование текста
hljs.configure({
    useBR: false
    });

var toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],
    ['blockquote', 'code-block'],
    [{ 'header': 1 }, { 'header': 2 }],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'indent': '-1'}, { 'indent': '+1' }],
    [{ 'color': [] }, { 'background': [] }],
    [{ 'align': [] }],
    ['formula'], ['link']
    ];

var quill = new Quill('#editor', {
  modules: {
    syntax: true,
    toolbar: toolbarOptions,
  },
  theme: 'snow',
  spellcheck: true,
  placeholder: 'Сообщение'
});

// Функции перетаскивания
Draggable.create(".user",{
    type:"x,y",
    onRelease:dropItem,
    autoScroll: 1
    });

    function dropItem(){
        var boundsBefore, boundsAfter;
        if (this.hitTest(".selected")){
            boundsBefore = this.target.getBoundingClientRect();
            $(this.target).appendTo('.selected');
            boundsAfter = this.target.getBoundingClientRect();
            TweenMax.fromTo(this.target, 0.2, {
                x:"+=" + (boundsBefore.left - boundsAfter.left), 
                y:"+=" + (boundsBefore.top - boundsAfter.top)
            }, { x:0, y:0 });
        } else {
            if (this.hitTest(".unselected")){
                boundsBefore = this.target.getBoundingClientRect();
            $(this.target).appendTo('.unselected');
            boundsAfter = this.target.getBoundingClientRect();
            TweenMax.fromTo(this.target, 0.2, {
                x:"+=" + (boundsBefore.left - boundsAfter.left), 
                y:"+=" + (boundsBefore.top - boundsAfter.top)
            }, { x:0, y:0 });
            filterFunction($('.dropdown-input')[0]);
            } else{
                TweenMax.to(this.target,0.2,{x:0,y:0});
            }
        }
    }