# 🧙 GitGoblin AI-Powered Commit Messages (Groq Edition)

GitGoblin now supports AI-generated commit messages using **Groq API**! Get descriptive, professional commit messages automatically generated based on your code changes - **blazingly fast** with Groq's lightning-speed inference!

## 🌟 Features

- **Intelligent Commit Messages**: AI analyzes your git diff and generates meaningful commit messages
- **Conventional Commits Format**: Follows best practices with types like `feat:`, `fix:`, `docs:`, etc.
- **Detailed Descriptions**: Complex changes get multi-line commit messages with bullet points
- **Lightning Fast**: Groq's LPU™ technology delivers responses in milliseconds
- **Automatic Fallback**: If AI fails, GitGoblin falls back to simple timestamp messages
- **Secure Storage**: API key is stored securely in `.git/gitgoblin.config.json`

## ⚡ Why Groq?

- **Speed**: 10-100x faster than traditional cloud AI APIs
- **Quality**: Uses powerful models like Llama 3.3 70B
- **Free Tier**: Generous free tier for personal projects
- **Reliability**: High uptime and consistent performance

## 🚀 Quick Start

### 1. Get Your Groq API Key

Visit [Groq Console](https://console.groq.com/) and create an account to get your API key for free!

### 2. Configure GitGoblin

```bash
# Set your API key (this also enables AI commits)
gitgoblin enchant --api-key gsk-your-api-key-here

# Verify configuration
gitgoblin enchant --show
```

### 3. Start Using AI Commits

```bash
# Start watching with AI-powered commits
gitgoblin summon

# Or force an AI-powered commit right now
gitgoblin sneak
```

## 📖 Configuration Commands

### Set API Key

```bash
gitgoblin enchant --api-key your_key
```

This automatically enables AI commits.

### Enable AI Commits

```bash
gitgoblin enchant --enable
```

### Disable AI Commits

```bash
gitgoblin enchant --disable
```

GitGoblin will use simple timestamp messages instead.

### Show Current Configuration

```bash
gitgoblin enchant --show
```

## 🎯 How It Works

1. **File Change Detected**: GitGoblin detects when you save a file
2. **Git Diff Analysis**: Extracts the changes using `git diff`
3. **AI Generation**: Sends the diff to Groq API (llama-3.3-70b-versatile model)
4. **Smart Commit**: Creates a commit with the AI-generated message
5. **Auto Push**: Pushes to GitHub automatically

## 💡 Example Commit Messages

### Before (without AI):

```
Modified src/app.py at 2026-02-03 16:30:45
```

### After (with AI):

```
feat: Add user authentication with JWT tokens

- Implement login and registration endpoints
- Add password hashing with bcrypt
- Create JWT token generation and validation
- Add middleware for protected routes
```

## 🔒 Security

- API keys are stored in `.git/gitgoblin.config.json` (automatically git-ignored)
- You can also use environment variable: `GROQ_API_KEY`
- Keys are never logged or displayed in full

## ⚙️ Advanced Configuration

### Using Environment Variable

```bash
# Windows PowerShell
$env:GROQ_API_KEY="gsk-your-key-here"
gitgoblin summon

# Linux/Mac
export GROQ_API_KEY="gsk-your-key-here"
gitgoblin summon
```

### Configuration File Location

The configuration is stored in:

```
your-repo/.git/gitgoblin.config.json
```

Example content:

```json
{
  "groq_api_key": "gsk-your-key-here",
  "ai_api_key": "gsk-your-key-here",
  "ai_commits_enabled": true
}
```

## 🎨 AI Model Details

**Model**: `llama-3.3-70b-versatile`

- 70 billion parameters
- Excellent at understanding code context
- Follows instructions precisely
- Generates concise, professional messages

**Prompt Engineering**:
The AI is prompted to follow these guidelines:

- Use conventional commits format (`feat:`, `fix:`, `docs:`, etc.)
- Keep first line under 72 characters
- Add detailed bullet points for complex changes
- Focus on the "why" and impact, not just the "what"
- Be specific and descriptive

## 🐛 Troubleshooting

### AI commits not working?

1. **Check API key is set:**

   ```bash
   gitgoblin enchant --show
   ```

2. **Verify AI is enabled:**

   ```bash
   gitgoblin enchant --enable
   ```

3. **Test API key manually:**
   ```bash
   gitgoblin sneak
   ```
   Watch for "🤖 Generating AI commit message..." output

### API errors?

- Verify your API key is valid at [Groq Console](https://console.groq.com/)
- Check your Groq account is active
- Ensure you have internet connection
- Check API rate limits (Groq has generous limits)

### Fallback behavior

If AI generation fails for any reason, GitGoblin automatically falls back to simple timestamp-based messages. Your commits will never be blocked!

## 💰 Cost Considerations

Groq offers an extremely generous free tier:

- **Free Tier**: 14,400 requests per day
- **Speed**: Responses in milliseconds
- **Cost**: Effectively free for most personal projects
- Each commit uses ~1 request
- Perfect for solo developers and small teams

## 🔄 Workflow Examples

### Solo Development

```bash
# One-time setup
gitgoblin enchant --api-key gsk-your-key-here

# Start working
gitgoblin summon

# Now every save gets an AI-generated commit!
```

### Team Project (disable AI)

```bash
# Disable AI for team projects
gitgoblin enchant --disable

# Use manual commits instead
git commit -m "Your team-approved message"
```

### Mixed Mode

```bash
# Use AI for auto-commits
gitgoblin summon

# But use custom messages for important commits
gitgoblin sneak --message "Release v2.0.0"
```

## 🎓 Best Practices

1. **Review AI Messages**: Check the generated messages occasionally to ensure quality
2. **Use for Solo Projects**: AI commits work best for personal projects
3. **Disable for Teams**: Teams often have specific commit message conventions
4. **Keep Diffs Small**: Smaller, focused changes get better AI descriptions
5. **Combine with Manual**: Use AI for auto-commits, manual for releases

## 🆚 Groq vs DeepSeek

| Feature     | Groq                         | DeepSeek                |
| ----------- | ---------------------------- | ----------------------- |
| Speed       | ⚡ Ultra-fast (milliseconds) | 🐢 Slower (1-3 seconds) |
| Free Tier   | ✅ Very generous             | ⚠️ Limited              |
| Model       | Llama 3.3 70B                | DeepSeek Chat           |
| Reliability | ✅ Excellent                 | ✅ Good                 |
| Cost        | 💰 Free for most use         | 💰 Pay per token        |

**GitGoblin now uses Groq by default for better performance!**

## 📚 Additional Resources

- [Groq Console](https://console.groq.com/)
- [Groq Documentation](https://console.groq.com/docs)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitGoblin Main README](README.md)

---

**Happy AI-powered committing with Groq! ⚡🤖👹**
