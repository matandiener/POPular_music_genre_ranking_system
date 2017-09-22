# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .models import Ranks
from django.views import generic

TITLE_GET_PARAM = 'title_q'
ARTIST_GET_PARAM = 'artist_q'
NUMBER_OF_RESULTS_GET_PARAM = 'num_of_results'


class IndexView(generic.ListView):
    template_name = 'ranking/index.html'
    context_object_name = 'highest_rank_list'

    def get_queryset(self):
        q = Ranks.objects.all()
        req = self.request.GET
        print req
        if TITLE_GET_PARAM in req:
            q = q.filter(title__icontains=req[TITLE_GET_PARAM]) if req[TITLE_GET_PARAM] else q
        if ARTIST_GET_PARAM in req:
            q = q.filter(artist__icontains=req[ARTIST_GET_PARAM]) if req[ARTIST_GET_PARAM] else q
        if NUMBER_OF_RESULTS_GET_PARAM in req and req[NUMBER_OF_RESULTS_GET_PARAM] > 0:
            return q[:req[NUMBER_OF_RESULTS_GET_PARAM]]
        return q
