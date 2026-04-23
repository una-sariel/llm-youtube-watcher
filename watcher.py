import yt_dlp
import time
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi

CHANNELS = [
    {"name": "Andrej Karpathy", "url": "https://www.youtube.com/@AndrejKarpathy"},
    {"name": "Yannic Kilcher", "url": "https://www.youtube.com/@YannicKilcher"},
    {"name": "Two Minute Papers", "url": "https://www.youtube.com/@TwoMinutePapers"},
    {"name": "Lex Fridman", "url": "https://www.youtube.com/@lexfridman"},
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
        transcript = transcript_list.find_transcript(['en'])
        fetched = transcript.fetch()
        text_parts = [snippet['text'] for snippet in fetched]
        return ' '.join(text_parts)[:800]
    except Exception as e:
        print(f"Transcript error: {str(e)[:100]}")
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
        if any(w in transcript_lower for w in ['transformer', 'attention', 'architecture']):
            topic = "LLM architecture explanation"
            points = ["Explains transformer/attention from transcript", "Technical deep dive"]
        elif any(w in transcript_lower for w in ['rlhf', 'alignment', 'safety']):
            topic = "LLM alignment and RLHF"
            points = ["Discusses model alignment from transcript", "Covers RLHF"]
        elif any(w in transcript_lower for w in ['paper', 'research', 'breakthrough']):
            topic = "AI research summary"
            points = ["Summarizes recent LLM research from transcript", "Explains breakthrough findings"]
        elif any(w in transcript_lower for w in ['interview', 'conversation', 'talk']):
            topic = "Expert AI/LLM interview"
            points = ["In-depth conversation from transcript", "Expert perspectives"]
        else:
            topic = "LLM educational content"
            points = ["Discusses LLM concepts from transcript", "Educational content"]
        points.append(f"Based on transcript analysis")
    else:
        title_lower = video_title.lower()
        if any(w in title_lower for w in ['gpt', 'transformer', 'attention']):
            topic = "LLM architecture (title-based)"
            points = ["Based on title: Transformer/attention", "Technical content"]
        elif any(w in title_lower for w in ['rlhf', 'alignment']):
            topic = "LLM alignment (title-based)"
            points = ["Based on title: RLHF/alignment", "Model safety"]
        elif any(w in title_lower for w in ['paper', 'research']):
            topic = "Research summary (title-based)"
            points = ["Based on title: Paper summary", "Research findings"]
        elif any(w in title_lower for w in ['interview', 'conversation']):
            topic = "Expert interview (title-based)"
            points = ["Based on title: Interview", "Expert perspectives"]
        else:
            topic = "LLM content (title-based)"
            points = ["Based on title: LLM concepts", "Educational content"]
        points.append("No transcript - title-based analysis")
    
    return {
        "speaker": channel_name,
        "main_topic": topic,
        "llm_key_points": points,
        "relation": relations.get(channel_name, "LLM channel"),
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
        body {{ font-family: Arial; margin: 40px; background: #f0f0f0; }}
        h1 {{ color: #333; }}
        table {{ width: 100%; border-collapse: collapse; background: white; }}
        th {{ background: #2c3e50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #ddd; vertical-align: top; }}
        .video-title a {{ color: #3498db; text-decoration: none; }}
        .key-point {{ margin: 5px 0; padding-left: 18px; position: relative; }}
        .key-point:before {{ content: "▹"; position: absolute; left: 0; color: #3498db; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-left: 8px; }}
        .badge-transcript {{ background: #27ae60; color: white; }}
        .badge-title {{ background: #e67e22; color: white; }}
        .footer {{ margin-top: 20px; text-align: center; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>LLM YouTube Watcher</h1>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Auto-refresh: hourly</p>
    <table><thead><tr><th>Speaker</th><th>Video</th><th>Main Topic</th><th>Key LLM Points</th><th>Channel Relation</th></tr></thead><tbody>"""
    
    for r in results:
        points_html = "".join([f'<div class="key-point">{p}</div>' for p in r['llm_key_points'][:3]])
        badge = '<span class="badge badge-transcript">Transcript</span>' if r['has_transcript'] else '<span class="badge badge-title">Title-based</span>'
        html += f"<tr><td><strong>{r['speaker']}</strong>{badge}</td><td><div class='video-title'><a href='{r['url']}' target='_blank'>{r['title'][:80]}</a></div></td><td>{r['main_topic']}</td><td>{points_html}</td><td>{r['relation']}</td></tr>"
    
    transcript_count = sum(1 for r in results if r['has_transcript'])
    html += f"</tbody></table><div class='footer'><p>{len(results)} videos | {transcript_count} with transcripts | {len(results)-transcript_count} title-based</p></div></body></html>"
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
    
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(generate_html(all_results))

if __name__ == "__main__":
    main()
