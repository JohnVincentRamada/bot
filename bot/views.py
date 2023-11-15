from django.shortcuts import render, redirect
from django.http import JsonResponse
import speech_recognition as sr
from django.views.decorators.csrf import csrf_exempt
import os
import pyttsx3
import torch
from django.shortcuts import render
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from sentence_transformers import SentenceTransformer
import pinecone
from bot.models import Log, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages


from transformers import T5Tokenizer, T5ForConditionalGeneration

from pprint import pprint

def home(request):
    
    return render(request, 'home.html')


def a_bot(request):
    
    if request.method == 'POST':
        result=request.POST["result"]
        pass_result = result
        pinecone.init(
        api_key="7e7d3e7c-8c84-4ad4-b662-c7cf67ef3384",
        environment="gcp-starter"  
        )
        index_name = "try-answer"

        
        
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
                output_ids = generator.generate(inputs["input_ids"], do_sample=True, num_beams=2, min_length=20, max_length=60)
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
        generated_answer = generate_answer(query)
        bot = generated_answer
       
        try:
            user_id = request.user.id
            
            
            if user_id is not None:
                user_instance = User.objects.get(pk=user_id)
                
                
                save_log = Log(user=user_instance, bot=bot, question=pass_result)
                save_log.save()
            else:
                
                print("Error: user_id is None")
        except User.DoesNotExist:
            
            print("Error: User with ID {} does not exist".format(user_id))
        except Exception as e:
            
            print(f"An error occurred: {e}")
        
        return render(request, 'a-bot.html', {'answer': bot})

    if request.user.is_authenticated:
        user = request.user
        firstname = user.first_name
        return render(request, 'a-bot.html', {'firstname': firstname})
    else:
        return redirect('login')
        
    

@csrf_exempt
def rectemplate(request):
    return render (request,'speechrecog.html')

@csrf_exempt
def recognize(request):
    if request.method == 'POST':
        recognizer = sr.Recognizer()
        audio_data = request.FILES['audio']

        try:
            with sr.AudioFile(audio_data) as source:
                audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return JsonResponse({'result': text})
        except sr.UnknownValueError:
            return JsonResponse({'error': 'Could not understand audio'})
        except sr.RequestError as e:
            return JsonResponse({'error': f'Error making the request: {e}'})

    return JsonResponse({'error': 'Invalid request method'})

def log(request):
    user = request.user.id
    messages = Log.objects.filter(user=user)
    return render(request, "log.html", {'conv': messages})

def request_context(request):
    if request.method == 'POST':
        context = request.POST["question"]
        comment = request.POST["comment"]

        request_context_instance = RequestContext(request=context,comment=comment)
        request_context_instance.save()
        messages.success(request, "Successfully Post Request")
        return redirect('log')
    return redirect('log')

    
