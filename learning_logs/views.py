from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Topic
from .forms import EntryForm, TopicForm


# Create your views here.
def home(request):
    """Returns the home page."""
    return render(request, 'index.html')


@login_required
def topics(request):
    """Returns the topics page."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'topics.html', context)


@login_required
def topic(request, topic_id):
    """Returns the specific topic page."""
    topic = Topic.objects.get(id=topic_id)
    
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'topic.html', context)


@login_required
def new_topic(request):
    """Returns the new topic page and adds the new topic."""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    
    context = {'form': form}
    return render(request, 'new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Returns the new entry page and adds the new entry."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic 
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
        
    context = {'topic': topic, 'form': form}
    return render(request, 'new_entry.html', context)