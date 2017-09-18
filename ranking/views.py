# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .models import Ranks
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'ranking/index.html'
    context_object_name = 'highest_rank_list'

    def get_queryset(self):
        return Ranks.objects.order_by('-rank')[:100]
