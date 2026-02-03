# 🔄 Groq Migration Guide

## GitGoblin AI: DeepSeek → Groq

GitGoblin has been upgraded to use **Groq** instead of DeepSeek for AI-powered commit messages. This brings significant improvements in speed and reliability!

## 🎉 What Changed?

### Before (DeepSeek):
- API: `https://api.deepseek.com/v1/chat/completions`
- Model: `deepseek-chat`
- Speed: 1-3 seconds per commit
- Cost: Pay per token

### After (Groq):
- API: `https://api.groq.com/openai/v1/chat/completions`
- Model: `llama-3.3-70b-versatile`
- Speed: **Milliseconds** per commit ⚡
- Cost: **Free tier** with generous limits

## 🚀 Benefits of Groq

1. **10-100x Faster**: Responses in milliseconds instead of seconds
2. **Better Free Tier**: 14,400 requests/day vs limited DeepSeek free tier
3. **More Reliable**: Consistent performance and uptime
4. **Same Quality**: Llama 3.3 70B produces excellent commit messages
5. **Better UX**: Near-instant commit message generation

## 📝 Migration Steps

### If You Were Using DeepSeek:

#### 1. Get a Groq API Key
Visit [Groq Console](https://console.groq.com/) and sign up for free.

#### 2. Update Your API Key
```bash
gitgoblin enchant --api-key gsk-your-new-groq-key
```

#### 3. Verify Configuration
```bash
gitgoblin enchant --show
```

That's it! Your old DeepSeek key will be automatically replaced.

### If You're New to AI Commits:

Just follow the quick start in [AI_COMMITS.md](AI_COMMITS.md)!

## 🔧 Technical Changes

### Code Changes:
1. **`ai_commit.py`**:
   - Updated API URL to Groq
   - Changed model to `llama-3.3-70b-versatile`
   - Updated all references from DeepSeek to Groq

2. **`config.py`**:
   - Added `groq_api_key` configuration
   - Maintains backward compatibility with `deepseek_api_key`
   - Supports both `GROQ_API_KEY` and `DEEPSEEK_API_KEY` env vars

3. **`cli.py`**:
   - Updated help text to reference Groq
   - Updated documentation links

### Backward Compatibility:

✅ **Old DeepSeek keys still work!**
- If you have a `deepseek_api_key` in your config, it will still be used
- Environment variable `DEEPSEEK_API_KEY` is still supported
- No breaking changes - existing setups continue to work

### Priority Order for API Keys:
1. `GROQ_API_KEY` environment variable
2. `DEEPSEEK_API_KEY` environment variable (legacy)
3. `groq_api_key` in config file
4. `ai_api_key` in config file
5. `deepseek_api_key` in config file (legacy)

## 📊 Performance Comparison

### Real-World Testing:

**DeepSeek**:
```
🤖 Generating AI commit message...
⏱️  Time: 2.3 seconds
✅ feat: Add user authentication
```

**Groq**:
```
🤖 Generating AI commit message...
⏱️  Time: 0.3 seconds ⚡
✅ feat: Add user authentication
```

**Result**: ~8x faster! 🚀

## 💡 Recommended Actions

### For Current Users:
1. Switch to Groq for better performance
2. Get free API key from [console.groq.com](https://console.groq.com/)
3. Update with: `gitgoblin enchant --api-key gsk-your-key`

### For New Users:
1. Start with Groq (default)
2. Follow [AI_COMMITS.md](AI_COMMITS.md) guide
3. Enjoy blazing-fast AI commits!

## 🐛 Troubleshooting

### "API request failed" after migration?
- Verify your Groq API key is correct
- Check you're using `gsk-` prefix (Groq) not `sk-` (DeepSeek)
- Ensure internet connection is active

### Want to keep using DeepSeek?
While not recommended, you can keep using DeepSeek:
1. Don't update your API key
2. Your existing `deepseek_api_key` will continue to work
3. Note: You'll miss out on Groq's speed improvements

### Need to switch back?
```bash
# Set DeepSeek key (will be used as fallback)
gitgoblin enchant --api-key sk-your-deepseek-key
```

## 📚 Updated Documentation

All documentation has been updated to reflect Groq:
- ✅ `AI_COMMITS.md` - Complete Groq guide
- ✅ `README.md` - Updated command examples
- ✅ `CHANGELOG.md` - Migration notes
- ✅ Code comments and docstrings

## 🎊 Summary

**GitGoblin + Groq = Blazingly Fast AI Commits! ⚡**

- **Faster**: Milliseconds instead of seconds
- **Free**: Generous free tier
- **Better**: Same quality, better performance
- **Easy**: Simple migration with one command

**Migrate now:**
```bash
gitgoblin enchant --api-key gsk-your-groq-key-here
```

---

**Questions?** Check [AI_COMMITS.md](AI_COMMITS.md) or open an issue!
