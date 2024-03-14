from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views import View
from utils.handle import handle_POST

from .models import Visitor


class VisitorView(View):
    template_name = 'visitor-form.html'

    def get(self, request, param=None, context={}):
        context['visitor'] = None
        context['form_title'] = 'CADASTRO DE VISITANTE'
        context['btn_label'] = 'Cadastrar'
        if param != 'novo':
            try:
                context['visitor'] = Visitor.objects.get(uuid=param)
                context['form_title'] = 'ATUALIZAÇÃO DE VISITANTE'
                context['btn_label'] = 'Atualizar'
            except:
                return HttpResponseNotFound(f'<h1>Visitante não encontrado!</h1><h2>id={param}</h2>')
        
        return render(request, self.template_name, context)
    
    def post(self, request, param=None):
        visitor = self.__valid_visitor(handle_POST(request.POST), param)
        if visitor:
            visitor.save()
        return redirect('visitante', param=visitor.uuid)
    
    def __valid_visitor(self, values, param):

        if param == 'novo':
            if visitor := Visitor.objects.filter(cpf=values['cpf']).first():
                return visitor
            visitor = Visitor()
        else:
            visitor = Visitor.objects.get(uuid=param)

        for k in values:
            setattr(visitor, k, values[k])

        return visitor
        