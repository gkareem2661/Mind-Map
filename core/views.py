import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Topic

# Create your views here.
def get_wiki_data(topic_name):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    HEADERS = {
        "User-Agent": "MindMapApp/1.0 (contact@example.com)"
    }

    # Search for the main topic to get the exact title and summary
    params_main = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": topic_name,
        "srlimit": 1
    }
    
    try:
        # Find best match for the main node
        R_main = S.get(url=URL, params=params_main, headers=HEADERS)
        data_main = R_main.json()
        
        if not data_main.get("query", {}).get("search"):
             return {"summary": "No results found.", "links": [], "title": topic_name}

        best_title = data_main["query"]["search"][0]["title"]
        page_id = data_main["query"]["search"][0]["pageid"]

        # Get Summary for the main node
        params_summary = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "pageids": page_id,
            "exintro": True,
            "explaintext": True,
        }
        R_summary = S.get(url=URL, params=params_summary, headers=HEADERS)
        data_summary = R_summary.json()
        summary = data_summary["query"]["pages"][str(page_id)].get("extract", "No summary available.")

        # Get related topics via "More Like This" search
        params_related = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": best_title, # Search for the title again
            "srlimit": 11, # Get top 11 (we will remove the self-match)
            "srprop": "", # We just want titles
        }
        
        R_related = S.get(url=URL, params=params_related, headers=HEADERS)
        data_related = R_related.json()
        
        related_results = data_related.get("query", {}).get("search", [])
        
        # Filter results to create the child links
        links = []
        for res in related_results:
            # Don't include the node itself in its children
            if res["title"] != best_title:
                links.append(res["title"])
        
        return {"summary": summary, "links": links, "title": best_title}

    except Exception as e:
        print(f"Error fetching Wiki data: {e}")
        return {"summary": f"Error: {str(e)}", "links": [], "title": topic_name}


def index(request):
    """Mind Map initial Page"""
    if request.user.is_authenticated:
        favorites = Topic.objects.filter(user=request.user).order_by('-created_at')
    else:
        favorites = Topic.objects.none()
    return render(request, 'index.html', {'favorites': favorites})

def topic_api(request):
    """Use JSON API for JS Mind Map to fetch data"""
    topic = request.GET.get('topic', 'Wikipedia')
    data = get_wiki_data(topic)
    return JsonResponse(data)

@login_required
def add_favorite(request):
    """Add a favorite"""
    if request.method == "POST":
        name = request.POST.get('name')
        summary = request.POST.get('summary')
        mind_map_json = request.POST.get('mind_map_data', '{}')
        
        if name:
            try:
                # Parse the mind map data JSON string
                mind_map_data = json.loads(mind_map_json) if mind_map_json else None
            except json.JSONDecodeError:
                mind_map_data = None
            
            Topic.objects.create(
                user=request.user,
                name=name, 
                summary=summary,
                mind_map_data=mind_map_data
            )
    return redirect('index')

@login_required
def delete_favorite(request, topic_id):
    """Delete a favorite"""
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    topic.delete()
    return redirect('index')

@login_required
def update_favorite(request, topic_id):
    """Edit user notes"""
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    if request.method == "POST":
        topic.user_notes = request.POST.get('user_notes')
        topic.save()
    return redirect('index')

@login_required
def load_mind_map(request, topic_id):
    """Get saved mind map data for a topic"""
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    if topic.mind_map_data:
        return JsonResponse({
            'success': True,
            'mind_map_data': topic.mind_map_data,
            'name': topic.name,
            'summary': topic.summary
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'No mind map data saved for this topic'
        })
