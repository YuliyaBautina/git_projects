from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.views import View

from NoticeBoard import settings
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
            send_mail(
                subject='Получен отклик',
                message=f'Здравствуйте! К вашему объявлению "{ post.title }" на сайте таверны "Копытом в рыло" оставлен отклик.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[replay.announce.author.user.email]
            )
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

    def get_success_url(self):
        return reverse_lazy('announce_detail', kwargs={'pk': self.object.announce.pk})


class ReplyDelete(DeleteView):
    model = Reply
    template_name = 'reply_delete.html'

    def get_success_url(self):
        return reverse_lazy('announce_detail', kwargs={'pk': self.object.announce.pk})

