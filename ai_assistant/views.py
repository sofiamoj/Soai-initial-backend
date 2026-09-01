from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import json
import httpx


SYSTEM_PROMPT = """You are the AI Assistant for SofiaAI — a personal brand by Sofia Mojahed,
a Django web developer and data scientist.

About SofiaAI:
- Services: AI Solutions (AI assistants, LLM integration, business automation),
  Data Analytics (dashboards, insights, predictive models),
  Web Development (scalable Django applications),
  Education & Training (hands-on coding courses for job seekers).
- Courses available: Python, Django, Data Science, AI Engineering — with interactive
  coding exercises (like a mini DataCamp).
- Contact: devhub4u@gmail.com, or via the Contact page on the site.
- The site is remote / worldwide based.

Your job:
- Answer visitor questions about these services and courses clearly and helpfully.
- If asked something unrelated to the site (general knowledge questions), you can still help,
  but gently steer back to how SofiaAI's services might be relevant when appropriate.
- Keep responses concise, friendly, and professional. Avoid making up details not listed above
  (like specific prices) — instead invite them to use the Contact page for specifics.
"""


class ChatView(View):
    def get(self, request):
        return render(request, 'ai_assistant/chat.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            print("=== AI VIEW CALLED ===")
            print("Message:", user_message)

            if not user_message:
                return JsonResponse({'response': 'Please type a message.'})

            # Build conversation history
            history = request.session.get('chat_history', [])
            messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
            for turn in history:
                messages.append({
                    'role': turn['role'],
                    'content': turn['content']
                })
            messages.append({'role': 'user', 'content': user_message})

            # Call OpenRouter API
            response = httpx.post(
                url='https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {settings.OPENROUTER_API_KEY}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'http://127.0.0.1:8000',
                    'X-Title': 'SofiaAI Assistant',
                },
                json={
                    'model': 'openrouter/free',
                    'messages': messages,
                    'max_tokens': 500,
                    'temperature': 0.7,
                },
                timeout=30.0
            )

            print("Status:", response.status_code)
            result = response.json()
            bot_response = result['choices'][0]['message']['content']
            print("Response:", bot_response[:50])

            # Save history (max 10 messages)
            history.append({'role': 'user', 'content': user_message})
            history.append({'role': 'assistant', 'content': bot_response})
            request.session['chat_history'] = history[-10:]

            return JsonResponse({'response': bot_response})

        except Exception as e:
            print("ERROR:", str(e))
            return JsonResponse({
                'response': 'Sorry, something went wrong. Please try again.'
            })
