# Telegram Notifier 🔔

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-success?style=flat&logo=githubactions)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=flat&logo=telegram)

A GitHub Action that sends beautifully formatted Telegram notifications for new issues and pull requests in your repository. Get instant alerts with comprehensive details, labels as hashtags, and clean formatting.

## ✨ Features

- **Instant Notifications**: Get real-time alerts for new events
- **Rich Formatting**: Clean HTML and MD formatting
- **Label Support**: Automatically converts GitHub labels to Telegram hashtags
- **Customizable**: Multiple configuration options for different needs
- **Reliable**: Built-in retry mechanism for Telegram API

## 🚀 Quick Start

### Basic Usage

```yaml
name: Event Notifier

on:
  issues:
    types: [opened, reopened]
  pull_request_target:
    types: [opened, reopened]

permissions:
  issues: read
  pull_request: read

jobs:
  notify:
    name: "Telegram notification"
    runs-on: ubuntu-latest
    steps:
      - name: Send Telegram notification for new issue or pull request
        uses: sehat1137/telegram-notifier@v1.4.0
        with:
          tg-bot-token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          tg-chat-id: ${{ vars.TELEGRAM_CHAT_ID }}
```

**Real usage examples:**
1. [FastStream](https://github.com/ag2ai/faststream/blob/main/.github/workflows/new-event.yaml)
2. [Dishka](https://github.com/reagento/dishka/blob/develop/.github/workflows/new-event.yml)

### Advanced Configuration

```yaml
- name: Send Telegram notification for new issue
  uses: sehat1137/telegram-notifier@v1.2.3
  with:
    tg-bot-token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    tg-chat-id: ${{ vars.TELEGRAM_CHAT_ID }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
    base-url: "https://github.com/your-org/your-repo"
    python-version: "3.10"
    attempt-count: "5"
    # if you have topics
    telegram-message-thread-id: 2
    # by default templates exist, these parameters override them
    html-template: "<b>New issue by <a href=/{user}>@{user}</a> </b><br/><b>{title}</b> (<a href='{url}'>#{id}</a>)<br/>{body}{labels}<br/>{promo}"
    md-template: '**New issue by [@{user}](https://github.com/{user})**\n**{title}** ([#{id}]({url}))\n\n{body}{labels}\n{promo}'
```

## 🔧 Setup Instructions

1. Create a Telegram Bot

- Message `@BotFather` on [Telegram](https://t.me/botfather)
- Create a new bot with `/newbot`
- Save the bot token

2. Get Chat ID

- Add your bot to the desired chat
- Send a message in the chat
- Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
- Find the chat.id in the response

3. Configure GitHub Secrets
   Add these secrets in your repository settings:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## 📋 Example Output

Your Telegram notifications will look like this:

Issue:
```text
🚀 New issue by @username
📌 Bug in authentication module (#123)

[Issue description content here...]

#bug #high_priority #authentication
sent via telegram-notifier
```

Pull requests:
```text
🎉 New Pull Request to test/repo by @username
✨ Update .gitignore (#3)
📊 +1/-0
🌿 Sehat1137:test → master

[Pull requests description content here...]

#bug #high_priority #authentication
sent via telegram-notifier
```

## 🤝 Acknowledgments

This action uses the excellent [sulguk](https://github.com/Tishka17/sulguk) library by `@Tishka17` for reliable Telegram message delivery. Special thanks to the author for creating and maintaining this wonderful library!
We also thank the authors of the [md2tgmd](https://github.com/yym68686/md2tgmd) library for their work. Special thanks to the authors for creating and maintaining these wonderful libraries!

## 🌟 Support

If you find this action useful, please consider:

- ⭐ Starring the repository on GitHub
- 🐛 Reporting issues if you find any bugs
- 💡 Suggesting features for future improvements
- 🔄 Sharing with your developer community

## 📝 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
