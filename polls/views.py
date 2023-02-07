from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, TemplateView

from .models import Question, Choice

class BaseIndexView(TemplateView):
    template_name = "polls/startpage.html"

    def get_context_data(self):
        questions = Question.objects.all()
        choices = Choice.objects.all()
        return {'message': 'WELCOME!!!', 'questions': questions, 'choices': choices}


class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class QuestionCreateView(CreateView):
    model = Question
    fields = ['question_text', 'pub_date']
    success_url = reverse_lazy('index')

class ChoiceCreateView(CreateView):
    model = Choice
    fields = ['question', 'choice_text', 'votes']
    success_url = reverse_lazy('index')
