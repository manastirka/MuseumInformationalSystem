# OpenAI API Reference - Correct Usage

## ⚠️ Common Mistakes to Avoid

The code snippet you showed has these issues:

```javascript
// ❌ INCORRECT - This is NOT the real OpenAI API
const response = await client.responses.create({
  model: "gpt-5.2",              // ❌ This model doesn't exist
  input: "Write a story...",     // ❌ Wrong parameter name
});
console.log(response.output_text); // ❌ Wrong response format
```

**Issues:**
1. ❌ `client.responses.create()` - Wrong API endpoint
2. ❌ `model: "gpt-5.2"` - This model doesn't exist (latest is GPT-4o)
3. ❌ `input:` - Should be `messages:`
4. ❌ `response.output_text` - Should be `response.choices[0].message.content`

---

## ✅ Correct OpenAI API Usage

### JavaScript/TypeScript (Node.js)

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// ✅ CORRECT
const response = await client.chat.completions.create({
  model: "gpt-4o",  // or "gpt-4-turbo", "gpt-3.5-turbo"
  messages: [
    {
      role: "system",
      content: "You are a helpful assistant."
    },
    {
      role: "user",
      content: "Write a short bedtime story about a unicorn."
    }
  ],
  temperature: 0.7,
  max_tokens: 500
});

console.log(response.choices[0].message.content);
```

### Python (Our Implementation)

```python
import requests

# ✅ CORRECT - This is what we're using
response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Write a short bedtime story about a unicorn."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
)

data = response.json()
assistant_message = data["choices"][0]["message"]["content"]
print(assistant_message)
```

### cURL (Direct API)

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Write a short bedtime story about a unicorn."
      }
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

---

## API Structure Breakdown

### Request Format

```json
{
  "model": "gpt-4o",           // Model to use
  "messages": [                // Array of messages
    {
      "role": "system",        // system, user, or assistant
      "content": "text"        // Message content
    },
    {
      "role": "user",
      "content": "text"
    }
  ],
  "temperature": 0.7,          // 0-2, controls randomness
  "max_tokens": 500,           // Maximum response length
  "top_p": 0.9,                // Nucleus sampling
  "frequency_penalty": 0,      // -2.0 to 2.0
  "presence_penalty": 0        // -2.0 to 2.0
}
```

### Response Format

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4o",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Once upon a time..."  // ← This is what you want!
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 150,
    "total_tokens": 170
  }
}
```

---

## Available Models (as of 2024)

### GPT-4 Series (Best Quality)
- `gpt-4o` - Latest, fastest GPT-4 model ✅ **Recommended**
- `gpt-4o-mini` - Smaller, cheaper GPT-4
- `gpt-4-turbo` - Previous generation
- `gpt-4` - Original GPT-4

### GPT-3.5 Series (Cheaper)
- `gpt-3.5-turbo` - Fast and affordable
- `gpt-3.5-turbo-16k` - Extended context

**Note:** There is NO "gpt-5.2" model!

---

## Our Museum System Implementation

Our `OpenAIProvider` class in `ai_api_providers.py` is **already using the correct format**:

```python
class OpenAIProvider(AIProvider):
    def chat(self, messages: List[Dict], options: Dict = None) -> Dict:
        """Send chat request to OpenAI API."""

        # ✅ Correct payload format
        payload = {
            'model': self.model,          # User-configured model
            'messages': messages,         # Messages array
            'temperature': options.get('temperature', 0.1),
            'max_tokens': options.get('max_tokens', 4096),
            'top_p': options.get('top_p', 0.9)
        }

        # ✅ Correct endpoint
        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=300
        )

        # ✅ Correct response parsing
        data = response.json()
        assistant_message = data['choices'][0]['message']['content']

        return {
            'success': True,
            'response': assistant_message,
            'usage': data.get('usage', {})
        }
```

---

## Message Roles Explained

### `system` Role
- Sets the behavior and context for the AI
- Usually the first message
- Example: "You are a museum curator specializing in mineralogy."

### `user` Role
- The human's input/question
- Example: "What minerals are in our collection?"

### `assistant` Role
- The AI's previous responses (for conversation history)
- Used to maintain context across multiple turns

### Example Conversation

```python
messages = [
    # System message sets the context
    {
        "role": "system",
        "content": "You are a helpful assistant for a museum."
    },

    # User asks a question
    {
        "role": "user",
        "content": "How many minerals do we have?"
    },

    # Assistant responds (from previous turn)
    {
        "role": "assistant",
        "content": "We have 5,997 mineral specimens."
    },

    # User asks follow-up
    {
        "role": "user",
        "content": "What's the most valuable one?"
    }
]
```

---

## Configuration in Museum System

When adding OpenAI provider in the system:

1. **Name**: `OpenAI GPT-4o` (friendly name)
2. **Type**: `openai`
3. **API Key**: `sk-proj-...` (from platform.openai.com)
4. **Model**: `gpt-4o` (select from dropdown)
5. **API Base** (optional): `https://api.openai.com/v1` (default)

The system will automatically:
- Use correct endpoint: `/chat/completions`
- Format messages correctly
- Parse responses correctly
- Track token usage

---

## Testing Your API Key

### Quick Test (cURL)

```bash
export OPENAI_API_KEY="sk-proj-..."

curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Say hello!"}],
    "max_tokens": 10
  }'
```

### Using Museum System

1. Add provider in configuration
2. Click **"Testiraj"** button
3. Should show green "Radi" status
4. Go to AI Assistant and send: "Hello!"

---

## Common Errors & Solutions

### Error: "Invalid model"
- ✅ Use: `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`
- ❌ Don't use: `gpt-5`, `gpt-5.2`, `text-davinci-003`

### Error: "Incorrect API key"
- Check your key at: https://platform.openai.com/api-keys
- Ensure it starts with `sk-proj-` or `sk-`
- Don't use organization ID as API key

### Error: "Rate limit exceeded"
- You've exceeded your quota or rate limit
- Check usage at: https://platform.openai.com/usage
- Consider upgrading your plan or using cheaper model

### Error: "Insufficient quota"
- Add billing details at: https://platform.openai.com/account/billing
- Add credits to your account
- Or use free alternative (Google Gemini)

---

## Cost Estimation

### GPT-4o (Recommended)
- Input: $2.50 / 1M tokens
- Output: $10.00 / 1M tokens
- ~$0.01 per typical query

### GPT-3.5-turbo (Cheaper)
- Input: $0.50 / 1M tokens
- Output: $1.50 / 1M tokens
- ~$0.001 per typical query

### Tips to Reduce Costs
1. Use `gpt-3.5-turbo` for simple queries
2. Use `gpt-4o-mini` instead of `gpt-4o`
3. Reduce `max_tokens` parameter
4. Clear conversation history regularly
5. Use system message to be concise

---

## Official Documentation

- **OpenAI Platform**: https://platform.openai.com/
- **API Reference**: https://platform.openai.com/docs/api-reference/chat
- **Model Pricing**: https://openai.com/api/pricing/
- **Usage Dashboard**: https://platform.openai.com/usage
- **API Keys**: https://platform.openai.com/api-keys

---

## Summary

✅ **Our implementation is CORRECT** - No changes needed
✅ **Using proper endpoint** - `/chat/completions`
✅ **Correct request format** - `messages` array
✅ **Correct response parsing** - `choices[0].message.content`
✅ **Supports all current models** - GPT-4o, GPT-4, GPT-3.5

The JavaScript code you showed was incorrect. Our Python implementation in `ai_api_providers.py` is already following the official OpenAI API specifications perfectly!
