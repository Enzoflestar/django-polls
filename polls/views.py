from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Question, Choice
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list
        }
    return render(request, "polls/index.html", context)

@login_required 
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    return HttpResponse(f"Resultados da pergunta de número {question_id}")

def vote(request, question_id):
    return HttpResponse(f"Você vai votar na pergunta de número {question_id}")

class QuestionCreateView(CreateView):
    model = Question 
    fields = ('question_text',)
    success_url = reverse_lazy('index')
    template_name = 'polls/question_form.html'

class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'

class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'

    from django.contrib import messages

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question 
    success_url = reverse_lazy("question_list")
    success_message ="Enquete excluída com sucesso!"

    def form_valid(self, form):
        message.success(self.request, self.success_message)
        return super().form_valid(form)

class QuestionUpdateView(UpdateView):
    model = Question
    templates_name = 'polls/question_form.html'
    success_url = reverse_lazy('question_list')
    success_message = 'Pergunta atualizada'
    fields = ('question-text', 'pub_date')

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando a pergunta'

        question_id = self.kwargs.get('pk')
        choices = Choice.objects.filter(question_pk=question_id)
        context['question_choices'] = choices

    def form_valid(self, request, *args, **kwargs):
        messages.sucess(self.request, self.success_message)
        return super(QuestionUpdateView, self).form_valid(request, *args, **kwargs)


