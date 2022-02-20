class CreateOrUpdateObject:
    """ Создает или обновляет объект на основе форм """
    def __init__(self, forms, object=None):
        self.forms = forms
        self.object = object
    
    def createObject(self, request):
        """ 
        Пытается создать объект на основе переданных форм. 
        Возвращает ошибки создания или созданный объект 
        """
        for creation_form in self.forms:
                form = creation_form(
                    request.POST, request.FILES, instance=self.object
                )
                if not form.is_valid():
                    if self.object: self.object.delete()
                    return form.errors
                self.object = form.save()
        return self.object
    
    def updateObject(self, request):
        """ 
        Пытается обновить объект на основе переданных форм. 
        Возвращает ошибки обновления или созданный объект 
        """
        for form_id in range(len(self.forms)):
            self.forms[form_id] = self.forms[form_id](
                request.POST, request.FILES, instance=self.object
            )
            if not self.forms[form_id].is_valid():
                return self.forms[form_id].errors
        [form.save() for form in self.forms]
        return self.object
   