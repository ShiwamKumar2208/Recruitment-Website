from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from crypt.models import CryptRecData
from charge.models import ChargeRecData
from credit.models import CreditRecData
from chronicle.models import ChronicleRecData
from create.models import CreateRecData
from clutch.models import ClutchRecData
from django.db.models import Q
import re

@login_required(login_url='/admin/login/')
def home(request):
    return render(request, 'useradmin/home.html')

@login_required(login_url='/admin/login/')
def index(request, **kwargs):
    return render(request, 'useradmin/search.html', {'signame' :kwargs.pop('sig_name')})


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


def get_query(query_string, search_fields):
    
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

@login_required(login_url='/admin/login/')
def search(request, **kwargs):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        sig_name=kwargs.pop('sig_name')
        entry_query = get_query(query_string, ['rollno', 'name','mobileno','email',])
        
        if sig_name == 'crypt':
            found_entries = CryptRecData.objects.filter(entry_query).order_by('name')
        elif sig_name == 'charge':
            found_entries = ChargeRecData.objects.filter(entry_query).order_by('name')
        elif sig_name == 'credit':
            found_entries = CreditRecData.objects.filter(entry_query).order_by('name')
        elif sig_name == 'chronicle':
            found_entries = ChronicleRecData.objects.filter(entry_query).order_by('name')
        elif sig_name == 'create':
            found_entries = CreateRecData.objects.filter(entry_query).order_by('name')
        elif sig_name == 'civil':
            found_entries = CivilRecData.objects.filter(entry_query).order_by('name')
        elif sig_name == 'clutch':
            found_entries = ClutchRecData.objects.filter(entry_query).order_by('name')
            
    return render(request, 'useradmin/results.html', { 'query_string': query_string, 'results': found_entries })

@login_required(login_url='/admin/login/')						  
def detailreply(request, **kwargs):
    sig_name = kwargs.pop('sig_name')
    query_id = kwargs.pop('pk')
    found_entry = None
    if sig_name == 'crypt':
        found_entry = CryptRecData.objects.get(id = query_id)
    elif sig_name == 'charge':
        found_entry = ChargeRecData.objects.get(id = query_id)
    elif sig_name == 'credit':
        found_entry = CreditRecData.objects.get(id = query_id)
    elif sig_name == 'chronicle':
        found_entry = ChronicleRecData.objects.get(id = query_id)
    elif sig_name == 'create':
        found_entry = CreateRecData.objects.get(id = query_id)
    elif sig_name == 'civil':
        found_entry = CivilRecData.objects.get(id = query_id)
    elif sig_name == 'clutch':
        found_entry = ClutchRecData.objects.get(id = query_id)
    
    return render(request, 'useradmin/detail.html', {'result': found_entry, 'signame': sig_name })
