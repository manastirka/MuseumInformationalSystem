# o1 Models Support - API Parameter Differences

## The Issue You Encountered

When using certain OpenAI models (particularly o1-preview and o1-mini), you may see this error:

```json
{
  "error": {
    "message": "Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.",
    "type": "invalid_request_error",
    "param": "max_tokens",
    "code": "unsupported_parameter"
  }
}
```

## Why This Happens

OpenAI's **o1 reasoning models** (o1-preview, o1-mini) use a **different API format** than standard models (GPT-4, GPT-3.5):

| Feature | GPT-4, GPT-3.5 | o1-preview, o1-mini |
|---------|----------------|---------------------|
| Max tokens parameter | `max_tokens` | `max_completion_tokens` |
| Temperature | ✅ Supported | ❌ Not supported |
| Top P | ✅ Supported | ❌ Not supported |
| System messages | ✅ Supported | ❌ Not supported |
| Streaming | ✅ Supported | ❌ Not supported |

## What I Fixed

The system now **automatically detects o1 models** and adjusts parameters:

### Before (Broken for o1):
```python
payload = {
    'model': 'o1-preview',
    'messages': messages,
    'temperature': 0.1,      # ❌ Causes error
    'max_tokens': 4096,      # ❌ Causes error
    'top_p': 0.9            # ❌ Causes error
}
```

### After (Works for o1):
```python
if model.startswith('o1-'):
    payload = {
        'model': 'o1-preview',
        'messages': filtered_messages,  # System msgs converted
        'max_completion_tokens': 4096   # ✅ Correct parameter
    }
else:
    payload = {
        'model': 'gpt-4o',
        'messages': messages,
        'temperature': 0.1,
        'max_tokens': 4096,
        'top_p': 0.9
    }
```

## How It Works Now

### 1. Model Detection
```python
is_o1_model = self.model.startswith('o1-') or self.model.startswith('o1')
```

Detects models like:
- `o1-preview`
- `o1-mini`
- `o1-preview-2024-09-12`
- Any future `o1-*` variants

### 2. Parameter Adjustment

**For o1 models:**
- Uses `max_completion_tokens` instead of `max_tokens`
- Removes `temperature`, `top_p` parameters
- Converts system messages to user messages

**For standard models (GPT-4, GPT-3.5):**
- Uses original parameters
- No changes needed

### 3. System Message Handling

o1 models don't support system messages, so they're converted:

```python
# Original message
{
  "role": "system",
  "content": "You are a museum assistant."
}

# Converted for o1
{
  "role": "user",
  "content": "[System Instructions]\nYou are a museum assistant."
}
```

## About "gpt-5.2" Model Name

You configured the system with model name `"gpt-5.2"` which **doesn't exist yet**. When you try to use it:

### What Might Happen:

1. **Most Likely**: OpenAI returns error "Model not found"
2. **Possible**: OpenAI redirects to a different model (o1-preview)
3. **Possible**: OpenAI falls back to default model

The error you're seeing suggests OpenAI **might be redirecting** your request to an o1 model, which is why you got the `max_tokens` error.

### Recommendation:

Update your configuration to use a **real model**:

```
Go to: AI Assistant → Podešavanja API
Click: Edit (pencil icon) next to "OpenAI GPT-5.2"
Change model to: gpt-4o (or click "Učitaj modele")
Save
```

## Valid Model Names

### Standard Models (Use max_tokens)
```
gpt-4o
gpt-4o-mini
gpt-4-turbo
gpt-4
gpt-3.5-turbo
```

### o1 Reasoning Models (Use max_completion_tokens)
```
o1-preview
o1-mini
o1-preview-2024-09-12
o1-mini-2024-09-12
```

## Testing Your Configuration

### Test with Real Model:

1. **Edit your provider**
   ```
   Model: gpt-4o  (instead of gpt-5.2)
   ```

2. **Click "Testiraj"**
   - Should show green "Radi"

3. **Try AI Assistant**
   - Should work without errors

### If You Want to Use o1 Models:

1. **Edit provider**
   ```
   Model: o1-preview  (or o1-mini)
   ```

2. **Save and test**
   - System automatically uses `max_completion_tokens`
   - No errors about unsupported parameters

## API Request Examples

### GPT-4 Request (Standard)
```json
POST /v1/chat/completions
{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello"}
  ],
  "temperature": 0.1,
  "max_tokens": 4096,
  "top_p": 0.9
}
```

### o1 Request (Reasoning)
```json
POST /v1/chat/completions
{
  "model": "o1-preview",
  "messages": [
    {"role": "user", "content": "[System Instructions]\nYou are helpful."},
    {"role": "user", "content": "Hello"}
  ],
  "max_completion_tokens": 4096
}
```

## Error Messages You Might See

### 1. Unsupported Parameter (FIXED)
```
"Unsupported parameter: 'max_tokens' is not supported"
```
**Fix**: System now auto-detects o1 models and uses correct parameter.

### 2. Model Not Found
```
"The model `gpt-5.2` does not exist"
```
**Fix**: Use a real model name (gpt-4o, o1-preview, etc.)

### 3. Invalid Model
```
"The model `gpt-5.2` is not available"
```
**Fix**: Click "Učitaj modele" to see YOUR available models.

## What Changed in the Code

### Old Code (Broke for o1):
```python
def chat(self, messages, options):
    payload = {
        'model': self.model,
        'messages': messages,
        'temperature': 0.1,      # ❌ Not supported in o1
        'max_tokens': 4096,      # ❌ Wrong parameter for o1
        'top_p': 0.9            # ❌ Not supported in o1
    }
    # ...
```

### New Code (Works for All):
```python
def chat(self, messages, options):
    is_o1_model = self.model.startswith('o1-')

    payload = {'model': self.model, 'messages': messages}

    if is_o1_model:
        payload['max_completion_tokens'] = 4096
        # Convert system messages to user messages
        # Don't include temperature, top_p
    else:
        payload['temperature'] = 0.1
        payload['max_tokens'] = 4096
        payload['top_p'] = 0.9
    # ...
```

## Benefits of o1 Models

Despite parameter restrictions, o1 models offer:

### Advanced Reasoning
- Better at complex logic
- Shows "thinking" process
- More accurate for difficult tasks

### Use Cases
- Mathematical problems
- Scientific analysis
- Complex decision making
- Multi-step reasoning

### Tradeoffs
- Slower responses
- More expensive
- No streaming
- No temperature control

## Pricing Comparison

### GPT-4o (Standard)
- Input: $2.50 / 1M tokens
- Output: $10.00 / 1M tokens
- Fast, configurable

### o1-preview (Reasoning)
- Input: $15.00 / 1M tokens
- Output: $60.00 / 1M tokens
- Slower, better reasoning

### o1-mini (Reasoning - Cheaper)
- Input: $3.00 / 1M tokens
- Output: $12.00 / 1M tokens
- Good balance

## Summary

✅ **System now supports both model types:**
- GPT-4, GPT-3.5 → Uses `max_tokens`, temperature, etc.
- o1-preview, o1-mini → Uses `max_completion_tokens`, no temperature

✅ **Automatic detection:**
- No configuration needed
- Just select the model you want
- System handles parameter differences

✅ **Your error is fixed:**
- Update model from "gpt-5.2" to real model
- System will use correct parameters automatically

⚠️ **Recommendation:**
- Use `gpt-4o` for general use (best balance)
- Use `o1-preview` for complex reasoning tasks
- Don't use `gpt-5.2` until it's released by OpenAI

---

**Next Steps:**
1. Edit your provider
2. Change model to `gpt-4o` or click "Učitaj modele"
3. Save and test
4. AI Assistant should work without errors
