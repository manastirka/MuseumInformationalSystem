# Dynamic Model Fetching - Feature Documentation

## Overview

The AI API Configuration now includes **automatic model discovery** using the official OpenAI Models API endpoint:
```
GET https://api.openai.com/v1/models
```

This means:
- ✅ **Automatically detects GPT-5.2** when it's released
- ✅ Shows only models available to YOUR account
- ✅ No manual updates needed for new models
- ✅ Works with custom OpenAI-compatible endpoints

## How It Works

### 1. Hardcoded Fallback Models (Default)

When you first open the configuration:
- Shows default list of known models
- Works without API key
- Safe fallback if API request fails

```javascript
// Default models shown
gpt-4o
gpt-4o-mini
gpt-4-turbo
gpt-4
gpt-3.5-turbo
o1-preview
o1-mini
```

### 2. Fetch Real Models (Dynamic)

After entering your API key:
1. Click **"Učitaj modele"** button
2. System calls OpenAI API: `GET /v1/models`
3. Filters for chat models (GPT-4, GPT-3.5, o1, GPT-5)
4. Replaces dropdown with YOUR available models

## Using the Feature

### Step-by-Step Guide

1. **Start Adding Provider**
   ```
   Go to: AI Assistant → Podešavanja API
   Click: "Dodaj Provider"
   ```

2. **Enter Basic Info**
   ```
   Name: OpenAI
   Type: openai
   API Key: sk-proj-xxxxx (paste your key)
   ```

3. **Click "Učitaj modele" Button**
   - Button appears next to Model dropdown
   - Requires API key to be entered first
   - Shows loading spinner

4. **View Your Available Models**
   - Dropdown updates with real models
   - Shows count: "Učitano X modela iz vašeg naloga"
   - Models sorted by name (newest first)

5. **Select Model**
   - Choose from your available models
   - Or use custom field to enter model manually

## What Models Are Detected

### Current Models (December 2024)
The system will show models like:
```
gpt-4o-2024-08-06
gpt-4o-2024-05-13
gpt-4o-mini-2024-07-18
gpt-4-turbo-2024-04-09
gpt-4-0613
gpt-3.5-turbo-0125
gpt-3.5-turbo-1106
o1-preview-2024-09-12
o1-mini-2024-09-12
```

### Future Models (Automatic)
When OpenAI releases new models:
```
gpt-5-2025-01-15        ← Will appear automatically
gpt-5.2-turbo           ← Will appear automatically
gpt-5.2-2025-03-01      ← Will appear automatically
```

The system checks for models matching these patterns:
- `gpt-4*` - All GPT-4 variants
- `gpt-3.5*` - All GPT-3.5 variants
- `o1*` - All o1 reasoning models
- `gpt-5*` - **Future GPT-5 models** ← Will be detected automatically!

## API Endpoint Used

### OpenAI Models API

```bash
# Request
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Response
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4o",
      "object": "model",
      "created": 1715367049,
      "owned_by": "system"
    },
    {
      "id": "gpt-5.2",  ← When released
      "object": "model",
      "created": 1735689600,
      "owned_by": "openai"
    }
    ...
  ]
}
```

### Python Implementation

```python
def get_models(self) -> List[str]:
    """Get available OpenAI models from API."""
    try:
        response = requests.get(
            f"{self.api_base}/models",
            headers={'Authorization': f'Bearer {self.api_key}'},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            chat_models = []
            for model in data.get('data', []):
                model_id = model.get('id', '')
                # Include GPT-4, GPT-3.5, o1, and GPT-5 models
                if any(prefix in model_id for prefix in ['gpt-4', 'gpt-3.5', 'o1', 'gpt-5']):
                    chat_models.append(model_id)

            chat_models.sort(reverse=True)
            return chat_models
        else:
            return self._get_fallback_models()

    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return self._get_fallback_models()
```

## Benefits

### 1. Future-Proof
- **No code updates needed** when GPT-5 is released
- Automatically detects new model versions
- Shows beta models if you have access

### 2. Accurate
- Shows **only models you can actually use**
- Respects account permissions
- No confusion about which models work

### 3. Convenient
- One click to refresh model list
- See exact model IDs (with dates)
- Know what's available without checking docs

### 4. Secure
- API key never leaves your server
- Uses official OpenAI endpoint
- Temporary provider instance for fetching

## Troubleshooting

### "Učitaj modele" Button Not Showing

**Cause**: Button only shows for OpenAI, Anthropic, Google providers
**Solution**: Select provider type first

### "Molimo unesite API ključ prvo"

**Cause**: API key field is empty
**Solution**: Enter your API key before clicking button

### Loading Spinner Never Stops

**Possible causes**:
1. Invalid API key
2. Network timeout
3. API endpoint unreachable

**Solution**:
- Check API key is correct
- Verify internet connection
- Check OpenAI status: https://status.openai.com

### No Models Shown

**Cause**: API returned empty list or error
**Solution**:
- Verify API key has permissions
- Check account status at platform.openai.com
- Fallback models will be shown instead

### Error: "The model X does not exist"

**Cause**: Model was in list but is deprecated/removed
**Solution**:
- Click "Učitaj modele" again to refresh
- Select a different model
- Use custom field to enter specific model

## When GPT-5.2 is Released

### What Will Happen Automatically:

1. **Click "Učitaj modele"**
   - System queries OpenAI API
   - Detects `gpt-5.2` in response
   - Adds to dropdown automatically

2. **You See:**
   ```
   Model dropdown:
   ┌─────────────────────────┐
   │ gpt-5.2                 │ ← New model appears!
   │ gpt-5-turbo             │
   │ gpt-4o                  │
   │ gpt-4o-mini             │
   │ ...                     │
   └─────────────────────────┘
   ```

3. **No Code Changes Needed**
   - The filter already includes `'gpt-5'`
   - Will match any `gpt-5*` model
   - Automatically sorted and displayed

### You Don't Need to Wait

If you want to prepare for GPT-5.2 now:

**Option 1: Use Custom Model Field**
```
Model: [Select any]
Custom Model: gpt-5.2
```

**Option 2: Configure Now, Update Later**
```
Add provider with gpt-4o now
When GPT-5.2 releases:
  1. Click "Učitaj modele"
  2. Select gpt-5.2
  3. Save
```

## Additional Features

### 1. API Key Visibility Toggle

Click the eye icon to show/hide your API key while typing:
```
[sk-proj-xxxxx] 👁️  ← Click to reveal
[sk-proj-12345] 👁️‍🗨️ ← Click to hide
```

### 2. Custom Model Override

Even after fetching models, you can enter custom model name:
```
Model: [Select from fetched list]
↓
Custom Model: gpt-5.2-experimental  ← Override
```

### 3. Loading Indicators

Visual feedback during fetch:
```
🔄 Preuzimam dostupne modele...
```

### 4. Success Confirmation

After successful fetch:
```
✓ Učitano 25 modela iz vašeg naloga
```

## Technical Details

### Backend Route

```python
@app.route('/api/ai/providers/fetch_models', methods=['POST'])
@login_required
def fetch_provider_models():
    """Fetch available models from provider API."""
    data = request.get_json()

    # Create temporary provider instance
    temp_config = {
        'type': data.get('type'),
        'api_key': data.get('api_key'),
        'model': 'temp'
    }

    provider = create_provider(temp_config)
    models = provider.get_models()

    return {'success': True, 'models': models}
```

### Frontend AJAX Call

```javascript
async function fetchAvailableModels() {
    const response = await fetch('/api/ai/providers/fetch_models', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            type: 'openai',
            api_key: apiKey
        })
    });

    const result = await response.json();
    // Update dropdown with result.models
}
```

## Security Considerations

### API Key Handling
- ✅ Sent over HTTPS only
- ✅ Used temporarily for fetching
- ✅ Not stored in browser
- ✅ Only accessible to logged-in users

### Provider Instance
- ✅ Created temporarily
- ✅ Destroyed after fetch
- ✅ No persistent storage
- ✅ Separate from active provider

## Comparison: Before vs After

### Before (Hardcoded)
```
✗ Only shows known models
✗ Need code update for new models
✗ Might show unavailable models
✗ Can't see beta access models
```

### After (Dynamic)
```
✓ Shows YOUR available models
✓ Auto-detects new releases
✓ Only shows usable models
✓ Includes beta models if you have access
```

## Summary

🎯 **Main Benefit**: When GPT-5.2 is released, you just need to:
1. Click "Učitaj modele"
2. Select "gpt-5.2"
3. Done!

No waiting for system updates, no manual configuration, no guessing if the model exists. The system automatically discovers and presents all models available to your account.

---

**Related Documentation**:
- `OPENAI_API_REFERENCE.md` - API usage details
- `AI_API_SETUP_GUIDE.md` - General setup guide
- `USING_CUSTOM_MODELS.md` - Custom model configuration
