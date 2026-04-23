import yt_dlp
import time
from datetime import datetime

CHANNELS = [
    {"name": "Andrej Karpathy", "url": "https://www.youtube.com/@AndrejKarpathy"},
    {"name": "Yannic Kilcher", "url": "https://www.youtube.com/@YannicKilcher"},
    {"name": "Two Minute Papers", "url": "https://www.youtube.com/@TwoMinutePapers"},
    {"name": "Lex Fridman", "url": "https://www.youtube.com/@lexfridman"},
]

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
                            'url': f"https://youtube.com/watch?v={entry.get('id', '')}",
                        })
                return videos
            return []
    except:
        return []

def analyze_video(video_title, channel_name):
    title_lower = video_title.lower()
    
    if any(w in title_lower for w in ['gpt', 'transformer', 'attention', 'architecture']):
        topic = "LLM architecture explanation"
        points = ["Explains transformer/attention mechanism", "Technical deep dive into LLMs"]
    elif any(w in title_lower for w in ['rlhf', 'alignment', 'safety', 'fine-tune']):
        topic = "LLM alignment and RLHF"
        points = ["Discusses model alignment techniques", "Covers reinforcement learning from human feedback"]
    elif any(w in title_lower for w in ['interview', 'conversation', 'discussion']):
        topic = "Expert AI/LLM interview"
        points = ["In-depth conversation about LLMs", "Expert perspectives on AI development"]
    elif any(w in title_lower for w in ['paper', 'research', 'breakthrough', 'new']):
        topic = "AI research summary"
        points = ["Summarizes recent LLM research", "Explains breakthrough findings"]
    else:
        topic = "LLM educational content"
        points = ["Discusses large language model concepts", "Provides AI/ML education"]
    
    relations = {
        "Andrej Karpathy": "Deep technical tutorials, builds from scratch",
        "Yannic Kilcher": "Paper reviews, RLHF and alignment focus",
        "Two Minute Papers": "Quick research summaries, latest breakthroughs",
        "Lex Fridman": "Long-form expert interviews"
    }
    
    return {
        "speaker": channel_name,
        "main_topic": topic,
        "llm_key_points": points,
        "relation": relations.get(channel_name, "LLM educational channel")
    }

def generate_html(results):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>LLM YouTube Watcher</title>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="3600">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }}
        h1 {{ color: #333; }}
        table {{ width: 100%; border-collapse: collapse; background: white; }}
        th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #ddd; vertical-align: top; }}
        .video-title a {{ color: #2196F3; text-decoration: none; }}
        .key-point {{ margin: 5px 0; padding-left: 15px; }}
        .footer {{ margin-top: 20px; text-align: center; color: #666; }}
    </style>
</head>
<body>
    <h1>LLM YouTube Watcher</h1>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Auto-refresh: hourly</p>
    <table>
        <thead>
            <tr><th>Speaker</th><th>Video</th><th>Main Topic</th><th>Key LLM Points</th><th>Channel Relation</th></tr>
        </thead>
        <tbody>"""
    
    for r in results:
        points_html = "".join([f'<div class="key-point">• {p}</div>' for p in r['llm_key_points']])
        html += f"""
            <tr>
                <td><strong>{r['speaker']}</strong></td>
                <td><div class="video-title"><a href="{r['url']}" target="_blank">{r['title'][:70]}</a></div></td>
                <td>{r['main_topic']}</td>
                <td>{points_html}</td>
                <td>{r['relation']}</td>
            </tr>"""
    
    html += f"""
        </tbody>
    </table>
    <div class="footer">
        <p>Data: YouTube (yt-dlp) | Analysis: Rule-based | {len(results)} videos</p>
    </div>
</body>
</html>"""
    return html

all_results = []
for channel in CHANNELS:
    videos = get_channel_videos(channel['url'], max_results=3)
    for video in videos:
        analysis = analyze_video(video['title'], channel['name'])
        all_results.append({
            "speaker": analysis['speaker'],
            "title": video['title'],
            "url": video['url'],
            "main_topic": analysis['main_topic'],
            "llm_key_points": analysis['llm_key_points'],
            "relation": analysis['relation']
        })
    time.sleep(0.5)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(generate_html(all_results))
