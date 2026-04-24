# LLM YouTube Watcher

## Problem Statement

Monitor popular YouTube channels focused on Large Language Models (LLMs) and automatically generate a categorized table analyzing video content. The solution must present results on a public webpage that updates automatically.

## Methodology

### Data Collection

The system uses `yt-dlp` to fetch the latest videos from each monitored channel. For each channel, the 3 most recent videos are retrieved.

**Monitored Channels:**
- Andrej Karpathy
- Yannic Kilcher
- Two Minute Papers
- Lex Fridman

### Content Analysis

The system uses **title-based keyword analysis** to categorize videos:

| Keyword Pattern | Assigned Topic |
|----------------|----------------|
| gpt, transformer, attention, architecture | LLM architecture explanation |
| rlhf, alignment, safety, fine-tune | LLM alignment and RLHF |
| paper, research, breakthrough, new | AI research summary |
| interview, conversation, discussion | Expert AI/LLM interview |
| (default) | LLM educational content |

### Channel Relation Mapping

| Channel | Relation Description |
|---------|---------------------|
| Andrej Karpathy | Deep technical tutorials, builds from scratch |
| Yannic Kilcher | Paper reviews, RLHF and alignment focus |
| Two Minute Papers | Quick research summaries, latest breakthroughs |
| Lex Fridman | Long-form expert interviews |

### Automation Pipeline

- **Platform**: GitHub Actions (free CI/CD)
- **Schedule**: Every 6 hours (cron: `0 */6 * * *`)
- **Hosting**: GitHub Pages
- **Page auto-refresh**: Every hour (meta refresh tag)

## Evaluation Dataset

- 4 channels × up to 3 videos = 12 videos per run
- Analysis period: April 2026

## Evaluation Methods

| Success Metric | Target |
|----------------|--------|
| Channel fetching | 100% success | 
| Dashboard generation | Success | 
| Public accessibility | Yes | 
| Hourly page refresh | Yes | 
| Scheduled automation | Every 6 hours | 
| Transcript acquisition | N/A | 

## Experimental Results

### Quantitative Results

| Metric | Value |
|--------|-------|
| Channels monitored | 4 |
| Videos analyzed per run | 10-12 |
| Transcripts acquired | 0 |
| GitHub Pages URL | Active |

### Sample Output Table

| Speaker | Video Title | Main Topic | Key Points | Channel Relation |
|---------|-------------|------------|------------|-------------------|
| Andrej Karpathy | How I use LLMs | LLM educational content | Discusses LLM concepts, AI education | Deep technical tutorials |
| Andrej Karpathy | Deep Dive into LLMs | LLM architecture explanation | Explains transformer/attention, Technical deep dive | Deep technical tutorials |
| Yannic Kilcher | Yannic Kilcher - Videos | LLM educational content | LLM concepts, AI education | Paper reviews, RLHF focus |
| Two Minute Papers | Two Minute Papers - Videos | AI research summary | Summarizes recent research, Explains findings | Quick research summaries |
| Lex Fridman | Lex Fridman - Videos | LLM educational content | LLM concepts, AI education | Long-form expert interviews |

### Transcript Acquisition Attempt

The system attempted to fetch transcripts using `youtube-transcript-api` but was unable to retrieve any captions. Possible reasons:

1. YouTube's automatic caption generation may not be enabled for these specific videos
2. The API library may be blocked by YouTube in automated environments
3. Video age or content type may affect subtitle availability

**Result**: 0 transcripts acquired across all tested videos. All analysis is based on video titles only.

### Limitations

- No transcripts available for analysis
- Analysis quality depends entirely on title accuracy
- Channel relation descriptions are static, not content-driven

### Future Improvements

- Identify videos with confirmed captions for testing
- Explore alternative subtitle extraction methods
- Implement LLM-based analysis when transcripts become available

## Live Demo

**[https://una-sariel.github.io/llm-youtube-watcher/index.html](https://una-sariel.github.io/llm-youtube-watcher/dashboard.html)**

## Repository

**https://github.com/una-sariel/llm-youtube-watcher**

## Repository Structure

