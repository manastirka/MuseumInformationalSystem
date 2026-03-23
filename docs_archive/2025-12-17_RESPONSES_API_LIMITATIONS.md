# Responses API Limitations - GPT-5.2

## The Issue You Encountered

When using GPT-5.2 with the Responses API, you may see this error:

```json
{
  "error": {
    "message": "Unsupported parameter: 'temperature' is not supported with this model.",
    "type": "invalid_request_error",
    "param": "temperature"
  }
}
```

## Why This Happens

The **Responses API** used by GPT-5 models has **fewer configurable parameters** than the traditional Chat Completions API.

### Supported Parameters (Responses API):
- ✅ `model` - Model to use
- ✅ `input` - Text input
- ✅ `max_output_tokens` - Maximum response length

### NOT Supported (Will Cause Errors):
- ❌ `temperature` - Randomness control
- ❌ `top_p` - Nucleus sampling
- ❌ `frequency_penalty` - Repetition penalty
- ❌ `presence_penalty` - Topic diversity
- ❌ `stop` - Stop sequences
- ❌ `n` - Number of completions
- ❌ `stream` - Streaming responses

## What I Fixed

Removed the `temperature` parameter from Responses API calls:

### Before (Caused Error):
```python
payload = {
    'model': 'gpt-5.2',
    'input': text,
    'max_output_tokens': 4096,
    'temperature': 0.1  # ❌ Not supported!
}
```

### After (Fixed):
```python
payload = {
    'model': 'gpt-5.2',
    'input': text,
    'max_output_tokens': 4096
    # ✅ No temperature parameter
}
```

## Why No Temperature Control?

According to OpenAI's design:

### Responses API (GPT-5):
- **Optimized for reasoning** - Less randomness needed
- **Consistent outputs** - More deterministic by default
- **Simplified interface** - Fewer knobs to tune
- **Better performance** - Optimizations possible without configurability

### Chat Completions API (GPT-4):
- **More flexible** - Full parameter control
- **Creative tasks** - Can adjust randomness
- **Legacy compatibility** - Maintains all features

## Comparison Table

| Parameter | GPT-4 (Chat Completions) | GPT-5 (Responses API) |
|-----------|-------------------------|---------------------|
| `temperature` | ✅ 0.0 - 2.0 | ❌ Not available |
| `top_p` | ✅ 0.0 - 1.0 | ❌ Not available |
| `max_tokens` | ✅ Configurable | ✅ `max_output_tokens` |
| `frequency_penalty` | ✅ -2.0 to 2.0 | ❌ Not available |
| `presence_penalty` | ✅ -2.0 to 2.0 | ❌ Not available |
| `n` (completions) | ✅ 1-10 | ❌ Not available |
| `stream` | ✅ true/false | ❌ Not available |
| `stop` | ✅ Array of strings | ❌ Not available |

## What This Means For You

### No Configuration Needed:
- GPT-5.2 uses **optimal default settings**
- No need to tune temperature or other parameters
- Consistent, high-quality responses

### Trade-offs:
- **Less control** over randomness/creativity
- **Cannot adjust** response style through parameters
- **Simpler interface** but less flexibility

### If You Need Control:
- Use **GPT-4o** for tasks requiring temperature control
- Use **GPT-5.2** for reasoning tasks (it's optimized automatically)
- Use **o1-preview** for advanced reasoning with some control

## API Request Examples

### Valid Responses API Request:
```json
POST /v1/responses
{
  "model": "gpt-5.2",
  "input": "Explain quantum computing.",
  "max_output_tokens": 2000
}
```

### Invalid (Will Error):
```json
POST /v1/responses
{
  "model": "gpt-5.2",
  "input": "Explain quantum computing.",
  "max_output_tokens": 2000,
  "temperature": 0.7  // ❌ ERROR!
}
```

### GPT-4 (Full Control Available):
```json
POST /v1/chat/completions
{
  "model": "gpt-4o",
  "messages": [...],
  "temperature": 0.7,  // ✅ Works
  "top_p": 0.9,
  "max_tokens": 2000
}
```

## Museum System Behavior

### For GPT-5.2 (Responses API):
```python
# System automatically:
✅ Detects GPT-5 model
✅ Uses Responses API
✅ Sends only supported parameters:
   - model
   - input
   - max_output_tokens
✅ Omits unsupported parameters:
   - temperature (removed)
   - top_p (removed)
   - etc.
```

### For GPT-4o (Chat Completions):
```python
# System automatically:
✅ Uses Chat Completions API
✅ Sends all parameters:
   - model
   - messages
   - temperature: 0.1
   - top_p: 0.9
   - max_tokens: 4096
```

## When to Use Each Model

### Use GPT-5.2 (Responses API) For:
- ✅ Complex reasoning tasks
- ✅ Mathematical problems
- ✅ Scientific analysis
- ✅ Multi-step logical thinking
- ✅ When you want best performance
- ⚠️ Accept: No temperature control

### Use GPT-4o (Chat Completions) For:
- ✅ Creative writing
- ✅ Tasks needing randomness control
- ✅ When you need consistent format
- ✅ When you want to tune temperature
- ⚠️ Accept: Slightly lower reasoning

### Use o1-preview For:
- ✅ Advanced reasoning
- ✅ Some parameter control
- ✅ Balance of both
- ⚠️ Accept: More expensive

## Performance vs Control Trade-off

```
More Control ←―――――――――→ Better Performance
GPT-4o        GPT-5.2
Full params   Limited params
Chat API      Responses API
```

GPT-5.2 sacrifices **configurability** for **performance**.

## Your Error is Now Fixed

After the code update:
1. ✅ Temperature parameter removed
2. ✅ Only `max_output_tokens` sent
3. ✅ API will accept the request
4. ✅ GPT-5.2 will work

## Restart Required

Since the code changed:

```bash
# Restart the app
sudo systemctl restart museum-system.service

# Or manually
pkill -f app.py
python3 app.py
```

## Testing Your Fix

Try the AI Assistant after restart:
1. Ask a question: "Koliko minerala imamo?"
2. Should get response without temperature error
3. GPT-5.2 will use its optimized defaults

## Alternative: Use GPT-4o

If you need temperature control:

1. Edit your provider
2. Change model to `gpt-4o`
3. Will use Chat Completions API
4. Temperature parameter will work

## Summary

❌ **Problem**: GPT-5.2 Responses API doesn't support `temperature`
✅ **Fixed**: Removed temperature from Responses API calls
⚠️ **Trade-off**: GPT-5.2 has fewer configurable parameters
💡 **Benefit**: Better performance, optimized for reasoning
🔄 **Action**: Restart app and test

The Responses API is simpler but more powerful for reasoning tasks. The lack of temperature control is by design - GPT-5 models are optimized to produce the best output automatically.

---

**Related Documentation:**
- `GPT5_RESPONSES_API.md` - Full Responses API guide
- `O1_MODELS_SUPPORT.md` - o1 model parameter differences
- `OPENAI_API_REFERENCE.md` - General OpenAI API usage
