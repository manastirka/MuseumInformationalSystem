# Bugfix: 'MuseumLLMAssistant' object has no attribute 'context_size'

## Error Message
```
Greška: Greška: 'MuseumLLMAssistant' object has no attribute 'context_size'
```

## Cause

When refactoring the `MuseumLLMAssistant` class to support multiple API providers, I removed the `context_size` parameter from `__init__()`:

### Before (Ollama-only)
```python
def __init__(self, model: str = "llama3.2:3b",
             context_size: int = 16384,
             ollama_host: str = "http://localhost:11434"):
    self.model = model
    self.context_size = context_size  # ✓ Defined
    self.ollama_host = ollama_host
```

### After Refactor (Broken)
```python
def __init__(self):
    self.provider = get_active_provider()
    # ✗ context_size not defined!
```

However, the `get_context_usage()` method still referenced `self.context_size`:

```python
def get_context_usage(self) -> Dict:
    return {
        'estimated_tokens': estimated_tokens,
        'max_tokens': self.context_size,  # ✗ AttributeError!
        'usage_percent': (estimated_tokens / self.context_size * 100),
        ...
    }
```

## Fix

Added `context_size` back to `__init__()`:

```python
def __init__(self):
    """Initialize the museum AI assistant with configured API provider."""
    self.provider = get_active_provider()
    self.conversation_history: List[Dict] = []
    self.current_context: Dict[str, Any] = {}
    self._last_lookup_metadata: Optional[Dict[str, Any]] = None
    self.context_size = 16384  # ✓ Default context size for tracking
```

## Why We Still Need It

Even though different AI providers have different context sizes (GPT-4: 128K, Claude: 200K, etc.), we keep a default `context_size` value for:

1. **Usage tracking** - Estimating conversation history size
2. **Backward compatibility** - Template expects this value
3. **Progress indicators** - Showing context usage percentage in UI

The actual context limits are handled by each provider's API, but we use this for display purposes.

## Files Changed

- ✓ `museum_llm_assistant.py` - Added `self.context_size = 16384` in `__init__()`

## Files Already Correct

- ✓ `app.py` - Already uses hardcoded `context_size=16384` in template render
- ✓ `templates/admin_ai_assistant.html` - Uses the value from template context

## Testing

```python
# This should now work:
assistant = get_museum_assistant()
usage = assistant.get_context_usage()
print(usage['max_tokens'])  # 16384
```

## Status

✅ **FIXED** - Error resolved, code compiles successfully

## Restart Required?

If the assistant instance is cached globally (`_assistant_instance`), you may need to restart the Flask app for changes to take effect:

```bash
# If running with gunicorn
sudo systemctl restart museum-system.service

# Or kill Python processes
pkill -f app.py
python3 app.py
```

## Related Changes

This was part of the migration from local Ollama to multi-provider API system. See:
- `AI_SYSTEM_MIGRATION_SUMMARY.md`
- `AI_API_SETUP_GUIDE.md`
