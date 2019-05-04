from __future__ import division
from redminelib import Redmine
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from rest_framework.decorators import action
from . models import feedbacks, analyzedFeedbacks, wish, democratic, account, related, game
import json
from django.http import JsonResponse
from django.core import serializers
from rest_framework import viewsets
from io import BytesIO
import re
import math
import datetime
import paralleldots
from. serializers import feedbacksSerializers, demoSerializers, wishSerializers, analyzedfeedbacksSerializers, accountSerializers, relatedFeedbacks, games


# Create your views here.

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


@login_required
def index(request):  # This function will be called on URL/cockpit
    feedback = feedbacks.objects.all()
    analyzedfeedback = analyzedFeedbacks.objects.all()
    return render(request, 'wish.html', {'feedback': feedback, 'analyzedfeedback': analyzedfeedback})

# These all are API views by Django Rest Framework


class feedbackView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = feedbacks.objects.all()
    serializer_class = feedbacksSerializers


class relatedFeedbacksView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = related.objects.all()
    serializer_class = relatedFeedbacks


class analyzedfeedbackView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = analyzedFeedbacks.objects.all()
    serializer_class = analyzedfeedbacksSerializers


class wishView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = wish.objects.all()
    serializer_class = wishSerializers


class demoView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = democratic.objects.all()
    serializer_class = demoSerializers


class accountView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = account.objects.all()
    serializer_class = accountSerializers


class gameView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = game.objects.all()
    serializer_class = games


@csrf_exempt
def postFeedback(request):  # Custom POST Feedback API
    if request.method == 'POST':
        category = request.POST.get("category")
        text = request.POST.get("text")[10:]
        text = text[:-2]
        bw = request.POST.get("bw")
        m = feedbacks(category=category, text=text, bw=bw)
        m.save()
        nlp(request)  # NLP function call
        return HttpResponse("Done!")
    else:
        return HttpResponse("Hello")


@csrf_exempt
def nlp(req):  # NLP work
    datetime = feedbacks.objects.latest('id').DateTime
    category = req.POST.get("category")
    text = req.POST.get("text")[10:]
    text = text[:-2]
    bw = req.POST.get("bw")
    fid = feedbacks.objects.latest('id').id
    counter = 0
    feedback = feedbacks.objects.order_by("id")[1:]
    for feedbac in feedback:
        if(classify(text) > 70):  # If its greater than 70 it means it's garbadge text
            return
        # Finds similar feedbacks
        if(feedbac.category.lower() == category.lower() and feedbac.bw.lower() == bw.lower()):
            paralleldots.set_api_key(
                "pCQlFdWiBwhGO8RERIGpwHDeAHQmWUjP3i9LLOrK0oc")  # Paralleldots API Key
            result = paralleldots.similarity(
                feedbac.text.lower(), text.lower())
            #print(result['similarity_score'])
            #If similarity score is greater than 0.5 It means they are same. You can change it
            if(result['similarity_score'] >= 0.65):
                counter = counter+1
                postToRelated(fid, feedbac.id)  # Post Related in related table
                return
# If we are here it means feedback is neither garbadge nor it's similar so we add it in analyzedfeedback table
    m = analyzedFeedbacks(
        DateTime=datetime, category=category, text=text, bw=bw, fid=fid, related=counter)
    m.save()


@csrf_exempt
def getRelated(request):
    ide = request.POST.get("id")
    idz = list()
    count = 0
    relatedFeed = related.objects.filter(followed=ide)
    for relatedF in relatedFeed:
        count = count+1
        idz.append(relatedF.follower)

    analyzedFeedbacks.objects.filter(fid=ide).update(related=count)
    return HttpResponse(json.dumps(idz), content_type="application/json")


@csrf_exempt
def postToRelated(follower, followed):
    if(followed == follower):
        print("Ignore")
    else:
        m = related(
            followed=followed, follower=follower)
        m.save()


@csrf_exempt
def postIssue(request):
    redmine = Redmine('http://demo.redmine.org',
                      username='Benjii60', password='dddse12345')
    project = redmine.project.get('dddse')
    subject = request.POST.get('id')
    des = request.POST.get('des')
    subject = "dddse_"+subject
    prID = request.POST.get('prID')
    issue = redmine.issue.create(
        project_id='dddse',
        subject=subject,
        description=des,
        priority_id=prID,
    )

    issue
    return HttpResponse(project.identifier)


@csrf_exempt
def logincheck(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    accounts = account.objects.all()
    for acc in accounts:
        if(acc.username == username and acc.password == password):
            return HttpResponse(json.dumps(acc), content_type="application/json")

    return HttpResponse("Invalid")

# Here is NLP functions donot change any of it


def split_in_chunks(text, chunk_size):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    if len(chunks) > 1 and len(chunks[-1]) < 10:
        chunks[-2] += chunks[-1]
        chunks.pop(-1)
    return chunks


def unique_chars_per_chunk_percentage(text, chunk_size):
    chunks = split_in_chunks(text, chunk_size)
    unique_chars_percentages = []
    for chunk in chunks:
        total = len(chunk)
        unique = len(set(chunk))
        unique_chars_percentages.append(unique / total)
    return sum(unique_chars_percentages) / len(unique_chars_percentages) * 100


def vowels_percentage(text):
    vowels = 0
    total = 0
    for c in text:
        if not c.isalpha():
            continue
        total += 1
        if c in "aeiouAEIOU":
            vowels += 1
    if total != 0:
        return vowels / total * 100
    else:
        return 0


def word_to_char_ratio(text):
    chars = len(text)
    words = len([x for x in re.split(r"[\W_]", text) if x.strip() != ""])
    return words / chars * 100


def deviation_score(percentage, lower_bound, upper_bound):
    if percentage < lower_bound:
        return math.log(lower_bound - percentage, lower_bound) * 100
    elif percentage > upper_bound:
        return math.log(percentage - upper_bound, 100 - upper_bound) * 100
    else:
        return 0


def classify(text):
    if text is None or len(text) == 0:
        return 0.0
    ucpcp = unique_chars_per_chunk_percentage(text, 35)
    vp = vowels_percentage(text)
    wtcr = word_to_char_ratio(text)

    ucpcp_dev = max(deviation_score(ucpcp, 45, 50), 1)
    vp_dev = max(deviation_score(vp, 35, 45), 1)
    wtcr_dev = max(deviation_score(wtcr, 15, 20), 1)

    return max((math.log10(ucpcp_dev) + math.log10(vp_dev) +
                math.log10(wtcr_dev)) / 6 * 100, 1)
