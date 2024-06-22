from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View

from users.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AnnounceForm, ReplyForm
from .models import Announce, Category, Reply


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('announce_list')


class AnnounceList(ListView):
    model = Announce
    ordering = '-date_time'
    template_name = 'announce_board.html'
    context_object_name = 'announce_board'
    paginate_by = 10


class AnnounceDetail(DetailView):
    model = Announce
    template_name = 'announce.html'
    context_object_name = 'announce'
    pk_url_kwarg = "pk"

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = ReplyForm(request.POST)
        if form.is_valid():
            replay = form.save(commit=False)
            replay.user = request.user
            replay.announce_id = post.pk
            replay.save()
            return redirect('announce_detail', pk=post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.reply_set.select_related('user', 'announce')
        context['reply_form'] = ReplyForm()
        context['comments'] = comments
        return context


class AnnounceCreate(LoginRequiredMixin, CreateView):
    # permission_required = ('board.add_announce', )
    form_class = AnnounceForm
    model = Announce
    template_name = 'announce_create.html'

    def form_valid(self, form):
        announce = form.save(commit=False)
        announce.author = self.request.user.author
        announce.save()

        return super().form_valid(form)


class AnnounceUpdate(LoginRequiredMixin,UpdateView):
    # permission_required = ('board.change_announce', )
    form_class = AnnounceForm
    model = Announce
    template_name = 'announce_edit.html'

    def dispatch(self, request, *args, **kwargs):
        announce = self.get_object()
        context = {'announce_id': announce.pk}
        if announce.author.user != self.request.user:
            return render(self.request, template_name='announce_lock.html', context=context)
        return super(AnnounceUpdate, self).dispatch(request, *args, **kwargs)


class AnnounceDelete(DeleteView):
    permission_required = ('board.delete_post',)
    model = Announce
    template_name = 'announce_delete.html'
    success_url = reverse_lazy('announce_list')

    def dispatch(self, request, *args, **kwargs):
        announce = self.get_object()
        context = {'announce_id': announce.pk}
        if announce.author.user != self.request.user:
            return render(self.request, template_name='announce_lock.html', context=context)
        return super(AnnounceDelete, self).dispatch(request, *args, **kwargs)


class ReplyUpdate(LoginRequiredMixin, UpdateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_edit.html'
    success_url = reverse_lazy('announce_list')

    # def dispatch(self, request, *args, **kwargs):
    #     reply = self.get_object()
    #     context = {'reply_id': reply.pk}
    #     if reply.user_id != self.request.user_id:
    #         return render(self.request, template_name='reply_lock.html', context=context)
    #     return super(ReplyUpdate, self).dispatch(request, *args, **kwargs)


class ReplyDelete(DeleteView):
    # permission_required = ('board.delete_post',)
    model = Reply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('announce_list')
