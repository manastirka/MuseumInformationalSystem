# Troubleshooting: Blank Response from AI Assistant

## Symptoms
- AI Assistant returns empty/blank field
- No error message shown
- Request succeeds but response is empty

## Possible Causes

### 1. Response API Format Issue
The Responses API might return data in a different format than expected.

### 2. Model Not Available
`gpt-5.2` might not be available in your OpenAI account yet.

### 3. API Endpoint Not Found
The `/v1/responses` endpoint might not be available.

### 4. Response Parsing Error
The response structure might be different than documented.

## Quick Fix: Try GPT-4o Instead

The easiest solution is to use a proven model:

### Step 1: Edit Provider
```
1. Go to: AI Assistant → Podešavanja API
2. Click: Edit (pencil icon) next to your provider
3. Change model to: gpt-4o
4. Save
```

### Step 2: Test
```
1. Go to AI Assistant
2. Ask: "Hello, can you hear me?"
3. Should get a response
```

GPT-4o is available to everyone and uses the well-tested Chat Completions API.

## Diagnostic Steps

### Step 1: Check Application Logs

```bash
# View logs
tail -f logs/museum_info_system.log

# Or if using systemd
journalctl -u museum-system.service -f
```

Look for lines like:
```
Responses API returned data: {...}
```

This shows what the API actually returned.

### Step 2: Check for Error Messages

Look for:
```
ERROR - Could not extract message from response
Empty response from API. Response structure: [...]
```

### Step 3: Check Response Structure

The log will show what fields are in the response:
```json
{
  "id": "...",
  "object": "...",
  "created": 123456,
  "output_text": "..."  // ← This is what we expect
}
```

## What I've Added

### Enhanced Response Parsing

The code now tries multiple response formats:

```python
assistant_message = (
    data.get('output_text') or        # Responses API format
    data.get('text') or               # Alternative format
    data.get('content') or            # Another alternative
    data.get('choices', [{}])[0]...   # Chat Completions format
)
```

### Better Error Messages

If response is empty, you'll now see:
```
Error: Empty response from API. Response structure: ['id', 'object', 'created', ...]
```

This tells you what fields exist.

### Automatic Fallback

If Responses API returns 404, automatically tries Chat Completions API.

## Manual Testing

### Test Responses API Directly

```bash
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "gpt-5.2",
    "input": "Say hello",
    "max_output_tokens": 100
  }'
```

### Test Chat Completions API

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 100
  }'
```

## Common Scenarios

### Scenario 1: GPT-5.2 Not Available Yet

**Symptoms:**
- Blank response
- No errors in logs
- API returns 200 OK

**Solution:**
```
Change model to: gpt-4o or o1-preview
```

### Scenario 2: Wrong API Endpoint

**Symptoms:**
- Error: 404 Not Found
- Log shows: "Responses API not available"

**Solution:**
```
System automatically falls back to Chat Completions
Or manually change to gpt-4o
```

### Scenario 3: Different Response Format

**Symptoms:**
- Blank response
- Log shows response structure without 'output_text'

**Solution:**
```
Code now tries multiple field names
Check logs for actual response structure
Report structure to developer
```

### Scenario 4: Empty Response from API

**Symptoms:**
- API returns 200 OK
- Response has empty text field

**Solution:**
```
1. Check API quota/billing
2. Try different prompt
3. Use different model
```

## Recommended Actions

### Immediate Fix (Use GPT-4o)

```
1. Edit provider configuration
2. Model: gpt-4o
3. Save and test
4. Should work immediately
```

### For Debugging (Keep GPT-5.2)

```
1. Restart app to get new code
2. Try AI Assistant
3. Check logs: tail -f logs/museum_info_system.log
4. Look for "Responses API returned data:"
5. Share log output for debugging
```

### Verify API Access

```bash
# Check which models you have access to
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY" | grep -E "gpt-5|gpt-4"
```

## Code Changes Made

### 1. Enhanced Response Parsing
```python
# Now tries multiple response formats
assistant_message = (
    data.get('output_text') or
    data.get('text') or
    data.get('content') or
    # ... fallbacks
)
```

### 2. Better Logging
```python
logger.info(f"Responses API returned data: {data}")
logger.error(f"Could not extract message from response: {data}")
```

### 3. Error Detection
```python
if not assistant_message:
    return {
        'success': False,
        'error': f'Empty response. Structure: {list(data.keys())}'
    }
```

### 4. Automatic Fallback
```python
if not result['success'] and '404' in result.get('error', ''):
    return self._chat_completions_api(messages, options)
```

## Next Steps

1. **Restart the application**
   ```bash
   sudo systemctl restart museum-system.service
   ```

2. **Try AI Assistant again**
   - If still blank, check logs
   - Share log output for debugging

3. **OR: Switch to GPT-4o** (Recommended)
   - Edit provider
   - Change model to `gpt-4o`
   - Guaranteed to work

## Why GPT-4o is Recommended

| Feature | GPT-5.2 | GPT-4o |
|---------|---------|--------|
| **Availability** | ❓ Uncertain | ✅ Available now |
| **API Support** | ❓ May not be ready | ✅ Fully supported |
| **Documentation** | ⚠️ Limited | ✅ Complete |
| **Testing** | ❓ Experimental | ✅ Production-ready |
| **Will it work?** | ❓ Unknown | ✅ Yes |

## Support

If you continue getting blank responses:

1. **Share these logs:**
   ```bash
   grep -A 5 "Responses API returned data" logs/museum_info_system.log
   ```

2. **Test which models work:**
   ```bash
   # In provider config, try each:
   - gpt-4o
   - gpt-4-turbo
   - gpt-3.5-turbo
   - o1-preview
   ```

3. **Check OpenAI status:**
   - https://status.openai.com

## Summary

**Quick Fix:** Change model to `gpt-4o` and it will work.

**For Debugging:**
1. Restart app
2. Try AI Assistant
3. Check `logs/museum_info_system.log`
4. Look for "Responses API returned data"
5. Share the response structure

The blank response likely means:
- GPT-5.2 not available yet, OR
- Response format different than expected, OR
- Responses API endpoint not ready

Using GPT-4o avoids all these issues.
