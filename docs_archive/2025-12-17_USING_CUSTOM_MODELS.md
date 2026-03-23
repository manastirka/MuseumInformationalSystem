# Using Custom Model Names (including GPT-5.2)

## ⚠️ Important Notice

**GPT-5.2 does not currently exist.** As of December 2024, OpenAI's latest models are:
- GPT-4o (newest)
- GPT-4-turbo
- GPT-4
- GPT-3.5-turbo

## However, You Can Now Enter Any Model Name

I've updated the system to allow custom model names. This is useful for:
1. **Future models** - When GPT-5 is released
2. **Beta access** - If you have early access to unreleased models
3. **Experimental models** - Models in testing phase
4. **Other providers** - Models not in the dropdown list

## How to Enter Custom Model Name

### Step 1: Add OpenAI Provider

1. Go to **AI Assistant** → **Podešavanja API**
2. Click **"Dodaj Provider"**
3. Fill in basic info:
   - **Name**: "OpenAI GPT-5.2" (or whatever you want)
   - **Type**: `openai`
   - **API Key**: Your OpenAI API key from https://platform.openai.com/api-keys

### Step 2: Select or Enter Model

You now have TWO options:

**Option A: Select from dropdown** (Recommended)
```
Model: gpt-4o ← Select from list
```

**Option B: Enter custom name** (New feature!)
```
Model: [Select any from dropdown first]
↓
Custom Model: gpt-5.2 ← Type your custom model here
```

The custom model field will override the dropdown selection.

### Step 3: Save and Test

1. Click **"Sačuvaj"**
2. Click **"Testiraj"** to test the connection

## What Will Happen

### If the Model Doesn't Exist

If you enter `gpt-5.2` but it doesn't exist yet, you'll get an error when you try to use it:

```json
{
  "error": {
    "message": "The model `gpt-5.2` does not exist",
    "type": "invalid_request_error",
    "code": "model_not_found"
  }
}
```

**The test will likely fail** and show a red "Greška" status.

### If You Have Beta Access

If OpenAI has given you access to a beta model:

```
Model: gpt-5-preview  ← If this exists in your account
```

The test should succeed and show green "Radi" status.

## Configuration Example for "GPT-5.2"

```
┌─────────────────────────────────────┐
│ Dodaj Provider                      │
├─────────────────────────────────────┤
│ Name: OpenAI GPT-5.2                │
│ Type: openai                        │
│ API Key: sk-proj-...                │
│ Model: [gpt-4o]  ← Select any       │
│ Custom Model: gpt-5.2  ← Type here  │
└─────────────────────────────────────┘
```

## Recommended Approach

### If GPT-5.2 doesn't exist yet:

1. **Use GPT-4o** now (best current model)
2. **Monitor OpenAI announcements** for GPT-5 release
3. **Update the model** when GPT-5.2 becomes available

### To stay updated:

- OpenAI Blog: https://openai.com/blog
- OpenAI Status: https://status.openai.com
- Model Documentation: https://platform.openai.com/docs/models

## Alternative: Use o1 Models

OpenAI recently released the **o1** series (reasoning models):

```
Model: o1-preview     ← Advanced reasoning
Model: o1-mini        ← Faster, cheaper reasoning
```

These are real models you can use right now.

## What If You Still Want to Try GPT-5.2?

I won't stop you, but here's what will happen:

1. ✅ Provider will be added successfully
2. ❌ Connection test will likely fail
3. ❌ Every AI query will return an error:
   ```
   "The model gpt-5.2 does not exist"
   ```
4. 🤷 The AI Assistant won't work until you change to a real model

## How to Update Model Later

If you configure "gpt-5.2" now and it gets released later:

1. Go to **Podešavanja API**
2. Find your provider
3. Click **"Testiraj"** again
4. If it now shows green "Radi", you're good to go!

Or if GPT-5.2 never materializes:

1. Click edit button (pencil icon)
2. Change model to `gpt-4o` or another real model
3. Save and test

## Current Model Recommendations

Since GPT-5.2 doesn't exist, use these instead:

### Best Quality
```
gpt-4o          ← Newest, smartest
gpt-4-turbo     ← Fast and capable
```

### Best Value
```
gpt-4o-mini     ← Cheaper GPT-4
gpt-3.5-turbo   ← Fastest, cheapest
```

### Best Reasoning
```
o1-preview      ← Advanced reasoning
o1-mini         ← Faster reasoning
```

## Testing Your Configuration

After saving your provider:

```bash
# The system will try this API call:
POST https://api.openai.com/v1/chat/completions
{
  "model": "gpt-5.2",  ← Your model
  "messages": [{
    "role": "user",
    "content": "test"
  }]
}

# If model doesn't exist, OpenAI returns:
{
  "error": {
    "message": "The model `gpt-5.2` does not exist",
    "type": "invalid_request_error"
  }
}
```

## Summary

✅ **You CAN enter "gpt-5.2"** - The system now allows custom model names
⚠️ **But it won't work** - Because the model doesn't exist yet
💡 **Alternative**: Use "gpt-4o" which is the latest and best available model
🔮 **Future-proof**: When GPT-5.2 is released, just update your configuration

## Need Help?

If you're not sure which model to use:

1. **Start with**: `gpt-4o` (best current model)
2. **For cheaper**: `gpt-3.5-turbo`
3. **For reasoning**: `o1-preview`
4. **For local/free**: Use Custom API with Ollama

Check your OpenAI account to see which models you have access to:
https://platform.openai.com/account/limits

---

**The system is ready to accept "gpt-5.2" as a model name, but it will not work until OpenAI releases that model.**
