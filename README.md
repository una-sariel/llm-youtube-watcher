# LLM YouTube Watcher

## Problem Statement
Monitor 4 popular YouTube channels focused on Large Language Models (LLMs) and automatically generate a categorized table analyzing video content.

## Methodology
- **Data Collection**: yt-dlp fetches latest videos from each channel
- **Content Analysis**: Rule-based keyword analysis on video titles
- **Auto Update**: GitHub Actions runs every 6 hours
- **Hosting**: GitHub Pages

## Monitored Channels
| Channel | Focus |
|---------|-------|
| Andrej Karpathy | LLM from scratch |
| Yannic Kilcher | Paper reviews / RLHF |
| Two Minute Papers | AI research news |
| Lex Fridman | Deep AI interviews |

## Live Demo
[https://una-sariel.github.io/llm-youtube-watcher/dashboard.html](https://una-sariel.github.io/llm-youtube-watcher/dashboard.html)

## Results
Successfully monitoring 4 channels. The dashboard updates every 6 hours via GitHub Actions and auto-refreshes hourly in the browser.

## Code
- `watcher.py`: Main script for fetching and analyzing videos
- `.github/workflows/update.yml`: Cron job configuration for scheduled updates
