# AI API Setup Guide

## Overview

The Museum Information System AI Assistant now supports multiple AI API providers instead of local Ollama. You can configure your own API credentials to use various AI services.

## Supported Providers

### 1. OpenAI (GPT-4, GPT-3.5)
- **API Key**: Get from https://platform.openai.com/api-keys
- **Models**: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo
- **Cost**: Pay-per-use
- **Recommended for**: Best quality, most reliable

### 2. Anthropic (Claude)
- **API Key**: Get from https://console.anthropic.com/
- **Models**: claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus
- **Cost**: Pay-per-use
- **Recommended for**: Best reasoning, long context

### 3. Google (Gemini)
- **API Key**: Get from https://makersuite.google.com/app/apikey
- **Models**: gemini-2.0-flash-exp, gemini-1.5-flash, gemini-1.5-pro
- **Cost**: Free tier available
- **Recommended for**: Free usage, good quality

### 4. OpenRouter
- **API Key**: Get from https://openrouter.ai/keys
- **Models**: Access to all major models through one API
- **Cost**: Pay-per-use
- **Recommended for**: Flexibility, model comparison

### 5. Custom API (Ollama, LM Studio, etc.)
- **API Base**: Your local or custom endpoint
- **Models**: Any model you're running
- **Cost**: Free (local)
- **Recommended for**: Privacy, no internet required

## Setup Instructions

### Step 1: Access Configuration Page

1. Log in to the Museum Information System
2. Go to **AI Assistant** page
3. Click **"Podešavanja API"** button

### Step 2: Add Provider

1. Click **"Dodaj Provider"**
2. Fill in the form:
   - **Naziv**: Friendly name (e.g., "OpenAI GPT-4")
   - **Tip Providera**: Select provider type
   - **API Key**: Enter your API key
   - **Model**: Select the model you want to use

3. For Custom API:
   - **API Base URL**: Your endpoint (e.g., `http://localhost:11434/v1`)
   - **Auth Header**: Usually "Authorization"
   - **Auth Prefix**: Usually "Bearer"

4. Click **"Sačuvaj"**

### Step 3: Activate Provider

1. The first provider you add will be automatically activated
2. To switch providers, click **"Aktiviraj"** next to any provider
3. Click **"Testiraj"** to verify the connection

### Step 4: Use AI Assistant

1. Go back to **AI Assistant** page
2. The active provider will be shown in the header
3. Start chatting with your museum data!

## Example Configurations

### OpenAI GPT-4o
```
Name: OpenAI GPT-4o
Type: openai
API Key: sk-...
Model: gpt-4o
```

### Anthropic Claude Sonnet
```
Name: Claude 3.5 Sonnet
Type: anthropic
API Key: sk-ant-...
Model: claude-3-5-sonnet-20241022
```

### Google Gemini (Free)
```
Name: Gemini Flash
Type: google
API Key: AIza...
Model: gemini-2.0-flash-exp
```

### Local Ollama
```
Name: Local Ollama
Type: custom
API Key: (any value)
Model: llama3.2:3b
API Base: http://localhost:11434/v1
Auth Header: Authorization
Auth Prefix: Bearer
```

## Security Notes

- API keys are stored locally in `data/api_providers.json`
- Never commit this file to version control
- Each user can configure their own providers
- API keys are not displayed in the UI after saving

## Troubleshooting

### Provider shows "Neaktivan"
- Check your API key is correct
- Verify you have credits/quota available
- Test the connection using the "Testiraj" button

### "Nema konfigurisan AI provider" error
- Go to API Configuration page
- Add at least one provider
- Activate the provider

### Connection timeouts
- Check your internet connection
- Verify the API endpoint is accessible
- For local providers (Ollama), ensure the service is running

## Cost Management

### Free Options
1. **Google Gemini**: Free tier with generous limits
2. **Local Ollama**: Completely free, runs locally
3. **OpenRouter**: Some models have free tiers

### Paid Options
1. **OpenAI**: Most expensive, best quality
2. **Anthropic**: Mid-range pricing, excellent reasoning
3. **OpenRouter**: Variable pricing based on model

### Tips
- Use cheaper models (GPT-3.5, Haiku) for simple queries
- Use premium models (GPT-4, Opus) for complex analysis
- Switch between providers based on needs
- Monitor usage in provider dashboards

## API Provider Links

- OpenAI: https://platform.openai.com/
- Anthropic: https://console.anthropic.com/
- Google: https://makersuite.google.com/
- OpenRouter: https://openrouter.ai/
- Ollama: https://ollama.ai/

## Support

For issues or questions:
1. Check provider status page
2. Verify API key validity
3. Test connection in configuration
4. Contact system administrator
