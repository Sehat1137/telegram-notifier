# Relator 🔔

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-success?style=flat&logo=githubactions)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=flat&logo=telegram)

**Relator** (Latin _referre_ - "to report") - delivers beautifully formatted GitHub notifications to Telegram. Get instant alerts for issues and PRs with smart labeling and clean formatting, keeping your team informed in real-time.

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
        uses: reagento/relator@v1.5.0
        with:
          tg-bot-token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          tg-chat-id: ${{ vars.TELEGRAM_CHAT_ID }}
          github-token: ${{ secrets.GITHUB_TOKEN }} # we recommend for use
```

> We recommend using a github-token, although it's not required for public projects and is unlikely to hit any [limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28#primary-rate-limit-for-unauthenticated-users). However, github actions uses IP-based limits, and since github actions has a limited pool of addresses, these limits are considered public, and you'll hit them very quickly.

### Advanced Configuration

```yaml
- name: Send Telegram notification for new issue
  uses: reagento/relator@v1.5.0
  with:
    tg-bot-token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    tg-chat-id: ${{ vars.TELEGRAM_CHAT_ID }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
    base-url: "https://github.com/your-org/your-repo"
    python-version: "3.10"
    attempt-count: "5"
    # if you want to join the input with a list of labels
    join-input-with-list: "1"
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
sent via relator
```

Pull requests:

```text
🎉 New Pull Request to test/repo by @username
✨ Update .gitignore (#3)
📊 +1/-0
🌿 Sehat1137:test → master

[Pull requests description content here...]

#bug #high_priority #authentication
sent via relator
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

## ⚙️ Used by

**Relator** is used by many open source projects here we highlight a few:

| Project                                                                        | Logo                                               | Description                                               |
| ------------------------------------------------------------------------------ | -------------------------------------------------- | --------------------------------------------------------- |
| [FastStream](https://github.com/ag2ai/faststream)                              | <img src=".static/faststream.png" width="45">      | FastStream is a powerful and easy-to-use Python framework |
| [Dishka](https://github.com/reagento/dishka)                                   | <img src=".static/reagento.png" width="45">        | Cute dependency injection (DI) framework for Python       |
| [wemake.services](https://github.com/wemake-services/wemake-python-styleguide) | <img src=".static/wemake-services.png" width="45"> | The strictest and most opinionated python linter ever!    |
