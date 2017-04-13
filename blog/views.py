from django.shortcuts import render
from django.utils import timezone
from .models import Post
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    tone_analyzer = ToneAnalyzerV3(
    username='a5fefc9c-a979-443f-8b07-8d9d92b9b2a3',
    password='vsNytjnc5sH3',
    version='2016-05-19 ')
    
    language_translator = LanguageTranslator(
    username='d5221880-eae5-4f09-a69b-f5111a7b8f99',
    password='2TFoeaud0HSY')


    #print(json.dumps(translation, indent=2, ensure_ascii=False))
	
    for post in posts:
        data = json.dumps(tone_analyzer.tone(text=post.text), indent=1)#converting to string and storing in the data
        j = json.loads(data);
        post.info = j['document_tone']['tone_categories'][0]['tones']
        #post.info = json.dumps(post.info);
        post.angerScore = post.info[0]['score']
        post.disgustScore = post.info[1]['score']
        post.fearScore = post.info[2]['score']
        post.joyScore = post.info[3]['score']
        post.sadScore = post.info[4]['score']
        #print(post.info[0]['tone_name'])
        translation = language_translator.translate(
        text=post.text,
        source='en',
        target='es')
        post.translatedText = json.dumps(translation, indent=2, ensure_ascii=False)
    return render(request, 'blog/post_list.html', {'posts': posts})