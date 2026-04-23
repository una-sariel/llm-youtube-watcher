import yt_dlp
import time
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi

CHANNELS = [
    {"name": "freeCodeCamp", "url": "https://www.youtube.com/@freecodecamp"},
    {"name": "Tech With Tim", "url": "https://www.youtube.com/@TechWithTim"},
    {"name": "Stanford Online", "url": "https://www.youtube.com/@stanfordonline"},
    {"name": "IBM Technology", "url": "https://www.youtube.com/@IBMTechnology"},
]


yt_api = YouTubeTranscriptApi()

def get_channel_videos(channel_url, max_results=3):
    ydl_opts = {'quiet': True, 'extract_flat': True, 'playlistend': max_results, 'socket_timeout': 10}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            if 'entries' in info:
                videos = []
                for entry in info['entries'][:max_results]:
                    if entry and entry.get('title'):
                        videos.append({
                            'title': entry.get('title', 'N/A'),
                            'video_id': entry.get('id', 'N/A'),
                            'url': f"https://youtube.com/watch?v={entry.get('id', '')}",
                            'published': entry.get('upload_date', 'N/A'),
                        })
                return videos
            return []
    except:
        return []

def get_video_transcript(video_id):
    try:
        transcript_list = yt_api.list(video_id)
        try:
            transcript = transcript_list.find_transcript(['en'])
            fetched = transcript.fetch()
            text = ' '.join([snippet['text'] for snippet in fetched])
            return text[:800]
        except:
            available_langs = [t.language_code for t in transcript_list]
            if available_langs:
                transcript = transcript_list.find_transcript([available_langs[0]])
                fetched = transcript.fetch()
                text = ' '.join([snippet['text'] for snippet in fetched])
                return text[:800]
            return None
    except:
        return None

def analyze_video(video_title, transcript, channel_name):
    relations = {
        "Andrej Karpathy": "Deep technical tutorials, builds from scratch",
        "Yannic Kilcher": "Paper reviews, RLHF and alignment focus",
        "Two Minute Papers": "Quick research summaries, latest breakthroughs",
        "Lex Fridman": "Long-form expert interviews"
    }
    
    if transcript:
        transcript_lower = transcript.lower()
        
        if any(w in transcript_lower for w in ['transformer', 'attention', 'architecture', 'neural network']):
            topic = "LLM architecture explanation"
            points = [
                "Explains transformer/attention mechanism from transcript",
                "Technical deep dive into LLM internals"
            ]
        elif any(w in transcript_lower for w in ['rlhf', 'alignment', 'safety', 'fine-tuning']):
            topic = "LLM alignment and RLHF"
            points = [
                "Discusses model alignment from transcript",
                "Covers reinforcement learning from human feedback"
            ]
        elif any(w in transcript_lower for w in ['paper', 'research', 'breakthrough', 'novel']):
            topic = "AI research summary"
            points = [
                "Summarizes recent LLM research from transcript",
                "Explains breakthrough findings"
            ]
        elif any(w in transcript_lower for w in ['interview', 'conversation', 'discussion', 'talk']):
            topic = "Expert AI/LLM interview"
            points = [
                "In-depth conversation about LLMs from transcript",
                "Expert perspectives on AI development"
            ]
        else:
            topic = "LLM educational content"
            points = [
                "Discusses large language model concepts from transcript",
                "Provides AI/ML educational content"
            ]
        
        points.append(f"Based on transcript analysis - {channel_name}")
    else:
        title_lower = video_title.lower()
        
        if any(w in title_lower for w in ['gpt', 'transformer', 'attention', 'architecture']):
            topic = "LLM architecture explanation (title-based)"
            points = ["Based on title: Explains transformer/attention", "Technical deep dive"]
        elif any(w in title_lower for w in ['rlhf', 'alignment', 'safety', 'fine-tune']):
            topic = "LLM alignment and RLHF (title-based)"
            points = ["Based on title: Discusses alignment", "RLHF content"]
        elif any(w in title_lower for w in ['interview', 'conversation', 'discussion']):
            topic = "Expert interview (title-based)"
            points = ["Based on title: In-depth conversation", "Expert perspectives"]
        elif any(w in title_lower for w in ['paper', 'research', 'breakthrough']):
            topic = "Research summary (title-based)"
            points = ["Based on title: Paper summary", "Research findings"]
        else:
            topic = "LLM content (title-based)"
            points = ["Based on title: LLM concepts", "Educational content"]
        
        points.append("(No transcript available - analysis based on title)")
    
    return {
        "speaker": channel_name,
        "main_topic": topic,
        "llm_key_points": points,
        "relation": relations.get(channel_name, "LLM educational channel"),
        "has_transcript": transcript is not None
    }

def generate_html(results):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>LLM YouTube Watcher</title>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="3600">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f0f0f0; }}
        h1 {{ color: #333; }}
        .sub {{ color: #666; font-size: 14px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        th {{ background: #2c3e50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #ddd; vertical-align: top; }}
        tr:hover {{ background: #f9f9f9; }}
        .video-title a {{ color: #3498db; text-decoration: none; font-weight: 500; }}
        .video-title a:hover {{ text-decoration: underline; }}
        .key-point {{ margin: 6px 0; padding-left: 18px; position: relative; font-size: 14px; }}
        .key-point:before {{ content: "▹"; position: absolute; left: 0; color: #3498db; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-left: 8px; }}
        .badge-transcript {{ background: #27ae60; color: white; }}
        .badge-title {{ background: #e67e22; color: white; }}
        .footer {{ margin-top: 20px; text-align: center; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>LLM YouTube Watcher</h1>
    <div class="sub">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC | Auto-refresh: hourly | Data: YouTube Transcript API</div>
    <table>
        <thead>
            <tr>
                <th style="width: 15%">Speaker</th>
                <th style="width: 25%">Video</th>
                <th style="width: 20%">Main Topic</th>
                <th style="width: 25%">Key LLM Points</th>
                <th style="width: 15%">Channel Relation</th>
            </tr>
        </thead>
        <tbody>"""
    
    for r in results:
        points_html = "".join([f'<div class="key-point">{p}</div>' for p in r['llm_key_points'][:3]])
        
        badge = '<span class="badge badge-transcript">Transcript</span>' if r['has_transcript'] else '<span class="badge badge-title">Title-based</span>'
        
        html += f"""
            <tr>
                <td><strong>{r['speaker']}</strong>{badge}</td>
                <td><div class="video-title"><a href="{r['url']}" target="_blank">{r['title'][:80]}</a></div></td>
                <td>{r['main_topic']}</td>
                <td>{points_html}</td>
                <td>{r['relation']}</td>
            </tr>"""
    
    transcript_count = sum(1 for r in results if r['has_transcript'])
    
    html += f"""
        </tbody>
    </table>
    <div class="footer">
        <p>{len(results)} videos analyzed | {transcript_count} with transcripts | {len(results) - transcript_count} title-based</p>
        <p>Monitored: Andrej Karpathy | Yannic Kilcher | Two Minute Papers | Lex Fridman</p>
    </div>
</body>
</html>"""
    return html

def main():
    all_results = []
    
    for channel in CHANNELS:
        videos = get_channel_videos(channel['url'], max_results=3)
        for video in videos:
            transcript = get_video_transcript(video['video_id'])
            analysis = analyze_video(video['title'], transcript, channel['name'])
            all_results.append({
                "speaker": analysis['speaker'],
                "title": video['title'],
                "url": video['url'],
                "main_topic": analysis['main_topic'],
                "llm_key_points": analysis['llm_key_points'],
                "relation": analysis['relation'],
                "has_transcript": analysis['has_transcript']
            })
            time.sleep(0.5)
    
    html_content = generate_html(all_results)
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
