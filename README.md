# Telegram Notifier 🔔

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-success?style=flat&logo=githubactions)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=flat&logo=telegram)

A GitHub Action that sends beautifully formatted Telegram notifications when new issues are created in your repository. Get instant alerts with issue details, labels as hashtags, and clean formatting.


## ✨ Features

* **Instant Notifications**: Get real-time alerts for new issues
* **Rich Formatting**: Clean HTML formatting with issue details
* **Label Support**: Automatically converts GitHub labels to Telegram hashtags
* **Customizable**: Multiple configuration options for different needs
* **Reliable**: Built-in retry mechanism for Telegram API


## 🚀 Quick Start

### Basic Usage

```yaml
name: issue

on:
  issues:
    types:
      - opened

jobs:
  notify:
    name: "Telegram notification"
    runs-on: ubuntu-latest
    steps:
      - name: Send Telegram notification for new issue
        uses: sehat1137/telegram-notifier@v1.0.0
        with:
          tg-bot-token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          tg-chat-id: ${{ env.TELEGRAM_CHAT_ID }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```
### Advanced Configuration

```yaml
- name: Send Telegram notification for new issue
  uses: sehat1137/telegram-notifier@v1.0.0
  with:
    tg-bot-token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    tg-chat-id: ${{ env.TELEGRAM_CHAT_ID }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
    base-url: "https://github.com/your-org/your-repo"
    python-version: "3.10"
    attempt-count: "5"
```

## 🔧 Setup Instructions
1. Create a Telegram Bot
* Message `@BotFather` on [Telegram](https://t.me/botfather)
* Create a new bot with `/newbot`
* Save the bot token
2. Get Chat ID
* Add your bot to the desired chat
* Send a message in the chat
* Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
* Find the chat.id in the response
3. Configure GitHub Secrets
Add these secrets in your repository settings:
* `TELEGRAM_BOT_TOKEN`
* `TELEGRAM_CHAT_ID`

## 📋 Example Output

Your Telegram notifications will look like this:

```text
🚀 New issue created by username

📌 Title: Bug in authentication module

🏷️ Tags: #bug #high_priority #authentication

🔗 Link: https://github.com/owner/repo/issues/123

📝 Description:
[Issue description content here...]
```

## 🤝 Acknowledgments

This action uses the excellent [sulguk](https://github.com/Tishka17/sulguk) library by `@Tishka17` for reliable Telegram message delivery. Special thanks to the author for creating and maintaining this wonderful library!


## 🌟 Support

If you find this action useful, please consider:

* ⭐ Starring the repository on GitHub
* 🐛 Reporting issues if you find any bugs
* 💡 Suggesting features for future improvements
* 🔄 Sharing with your developer community


## 📝 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
