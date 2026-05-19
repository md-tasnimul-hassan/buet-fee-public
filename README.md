# BUET Dining Fee Notifier

My hall in BUET post due fee notices in physical notice boards that i had little patience to check every few days. So one weekend's night, I built a bot that checks everyone's balance daily and emails them automatically if anything is due. It has been running in production since February, 2026.

## How it works

The script launches a headless Chromium engine **Playwright** and navigates
Bank's BUET fee portal. It fills in the student ID and fee type and necessary details. **BeautifulSoup** then
parses the page HTML to extract the student name and outstanding amount.

If there is due amount, a styled HTML email is composed using Python's
**smtplib** and **MIME** libraries and sent via Gmail SMTP. Both a plain-text 
fallback and an HTML version are attached so it renders correctly across all 
email clients.

## Automation

The entire thing runs on **GitHub Actions** with a daily cron trigger — no server, no hosting, zero maintenance after deployment. YaY !

```yaml
on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
```

The Gmail credentials are stored as **GitHub Actions Secrets** and injected into the environment at runtime. They never appear anywhere in the codebase.

## Privacy

The student database is private, gitignored, and never committed to this repository.
Only students who explicitly opted in are included. If you're a current BUET student and 
want to be added to the notification list, feel free to reach out. :) 

## Future Error Handling

If anything fails during a run — network timeout, site structure change, anything — the bot emails me directly with the error so I can fix it. 
No silent failures.

## Stack

Python · Playwright · BeautifulSoup · smtplib · GitHub Actions
