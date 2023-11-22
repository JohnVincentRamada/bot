from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from customadmin.models import Description
from bot.models import RequestContext
import pinecone
from sentence_transformers import SentenceTransformer
import os
import torch
import pandas as pd
from .forms import DescriptionForm, UserForm
import pyttsx3

from transformers import T5Tokenizer, T5ForConditionalGeneration

from pprint import pprint

pinecone.init(api_key="7e7d3e7c-8c84-4ad4-b662-c7cf67ef3384", environment="gcp-starter")
index = pinecone.Index(index_name='try-answer')




def admin_login(request):

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists ():
            messages.error(request, 'Account not found')
            return(redirect('admin_login'))
        
        user_obj = authenticate(username=username, password=password)

        if user_obj and user_obj.is_superuser:
            login(request, user_obj)
            
            return(redirect('dashboard/'))
        
        messages.error(request, 'Invalid Password')
        return redirect('admin_login')

    return render(request, 'custom_admin/login.html')

def dashboard(request):

    if request.user.is_authenticated and request.user.is_superuser:
        user_detail = User.objects.get(first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email)
        requests = RequestContext.objects.all()
        total_applied = RequestContext.get_applied_count()
        total_pending = RequestContext.get_pending_count()
        total_request = RequestContext.get_total_count()
        total_pending_percentage = (total_pending / total_request) * 100 if total_request != 0 else 0
        total_applied_percentage = (total_applied / total_request) * 100 if total_request != 0 else 0
        context = {
            "data": user_detail,
            "requests": requests, 
            "total_applied": total_applied,
            "total_pending": total_pending,
            "total_request": total_request,
            'total_pending_percentage': total_pending_percentage,
            'total_applied_percentage': total_applied_percentage,
        }

        return render(request, 'custom_admin/dashboard.html', context)
    else:
        return redirect('admin_login')

# user
def user(request):

    if request.user.is_authenticated and request.user.is_superuser:
        users = User.objects.filter(is_superuser=False)
        user_detail = User.objects.get(first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email)

        return render(request, 'custom_admin/user.html', {'users': users, 'data': user_detail})
    else:
        return redirect('admin_login')

def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)   
        if form.is_valid():
            form.save()
            messages.success(request,"Succefully Update User")
            return redirect('user')
    return render(request, 'custom_admin/user_update.html', {'form': form, 'user': user})

def delete_user(request):
    if request.method == 'POST':
        pk = request.POST.get('userpk')
        print(pk)
        print("asdfasdf")
        intpk = int(pk)
        print(pk)
        user = User.objects.get(id=intpk)
        user.delete()
        messages.success(request,'User Deleted Successfuly!')
    return redirect('user')

# description
def description(request):

    if request.user.is_authenticated and request.user.is_superuser:
        description = Description.objects.all()
        
            
        
        user_detail = User.objects.get(first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email)
        return render(request, 'custom_admin/description.html', {'description': description,'data': user_detail})
    else:
        return redirect('admin_login')
def add_description(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = DescriptionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, "Successfully Added New Description")
                return redirect('description') 
        else:
            form = DescriptionForm()
        user_detail = User.objects.get(first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email)
        return render(request, 'custom_admin/add_description.html', {'data': user_detail, 'form': form})
    else:
        return redirect('admin_login')

def edit_description(request, pk):
    description = Description.objects.get(pk=pk)
    form = DescriptionForm(instance=description)
    if request.method == 'POST':
        form = DescriptionForm(request.POST, instance=description)   
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully Update Description")
            return redirect('description')
    return render(request, 'custom_admin/Description_update.html', {'form': form, 'description': description})

def delete_description(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        description = Description.objects.get(id=pk)
        description.delete()
        messages.success(request,"Successfully Delete Description")
    return redirect('description')


# testabot
def testabot(request):

    if request.user.is_authenticated and request.user.is_superuser:
        user_detail = User.objects.get(first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email)
        if request.method == 'POST':
            result=request.POST["result"]
            pinecone.init(
            api_key="7e7d3e7c-8c84-4ad4-b662-c7cf67ef3384",
            environment="gcp-starter"  # find next to API key in console
            )
            index_name = "try-answer"

            # check if the abstractive-question-answering index exists
            
            index = pinecone.Index(index_name)

            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            retriever = SentenceTransformer("flax-sentence-embeddings/all_datasets_v3_mpnet-base", device=device)
            retriever
            tokenizer = T5Tokenizer.from_pretrained("model")
            generator = T5ForConditionalGeneration.from_pretrained("model")
            
            def query_pinecone(query, top_k):
                # generate embeddings for the query
                xq = retriever.encode([query]).tolist()
                # search pinecone index for context passage with the answer
                xc = index.query(xq, top_k=top_k, include_metadata=True)
                return xc
            def format_query(query, context):
                # extract passage_text from Pinecone search result and add the <P> tag
                context = [f"{m['metadata']['Answer']}" for m in context]
                # concatinate all context passages
                context = " ".join(context)
                # contcatinate the query and context passages
                query = f"question: {query} context: {context}"
                return query
            def generate_answer(query):
                # Tokenize the query to get input_ids
                inputs = tokenizer(query, return_tensors="pt", max_length=1024, truncation=True)
                # Use the model to predict output ids
                with torch.no_grad():
                    output_ids = generator.generate(inputs["input_ids"], num_beams=2, min_length=20, max_length=60)
                # Use the tokenizer to decode the output ids
                answer = tokenizer.decode(output_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[1].id)
                engine.say(answer)
                engine.runAndWait()
                return answer
                

            
            query = result
            result = query_pinecone(query, top_k=3)
            query = format_query(query, result["matches"])
            generate_answer(query)

            return render(request, 'custom_admin/testabot.html', {'query': query})
        return render(request, 'custom_admin/testabot.html', {'data': user_detail})
    else:
        return redirect('admin_login')

def dashboard_apply(request, pk):
    
    if request.user.is_authenticated and request.user.is_superuser:
        user_detail = User.objects.get(first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email)
        apply_request = RequestContext.objects.get(pk=pk)
        if request.method == 'POST':
            form = DescriptionForm(request.POST)
            if form.is_valid():
                form.save()
                apply_request.status = 'applied'
                apply_request.save()
                messages.success(request,"Successfully Applied Request")
                return redirect('dashboard') 
        else:
            form = DescriptionForm()
            

        return render(request, 'custom_admin/dashboard_apply.html', {'data': user_detail, 'form': form, 'apply_request': apply_request})
    else:
        return redirect('admin_login')


def signout(request):
    logout(request)
    return redirect('admin_login')