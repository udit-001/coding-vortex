from django.shortcuts import render, HttpResponse, redirect
from .forms import ContactForm
from .models import Contact
from django.views import View
from django.contrib import messages


class ContactView(View):
    def get(self, request):
        context = {
            'form': ContactForm()
        }
        return render(request, 'contacts/contact.html', context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message was sent successfully!')
            return redirect('contact')
        else:
            context = {
                'form': form
            }
            return render(request, 'contacts/contact.html', context)
        return HttpResponse('Ok')
