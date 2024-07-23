import json
import asyncio

from aiohttp import web


async def generate_response(prompt):
    # This is a mock function. Replace with your actual generation logic.
    words = prompt.split()
    for word in words:
        yield f'This is a response to: {word}\n'
        await asyncio.sleep(0.5)  # Simulate delay


async def chat_completions(request):
    data = await request.json()
    messages = data['messages']
    model = data['model']
    frequency_penalty = data.get('frequency_penalty')
    logit_bias = data.get('logit_bias')
    logprobs = data.get('logprobs', False)
    top_logprobs = data.get('top_logprobs')
    max_tokens = data.get('max_tokens')
    n = data.get('n', 1)
    presence_penalty = data.get('presence_penalty')
    response_format = data.get('response_format') # TODO: https://platform.openai.com/docs/api-reference/chat/create#chat-create-response_format
    seed = data.get('seed')
    temperature = data.get('temperature', 0.0)
    stream = data.get('stream', False)

    assert frequency_penalty is None
    assert logit_bias is None
    assert logprobs == False
    assert top_logprobs is None
    assert max_tokens is None or isinstance(max_tokens, int)
    assert n == 1
    assert presence_penalty is None
    assert response_format is None
    assert seed is None or isinstance(seed, int)


    prompt = messages[-1]['content']

    if stream:
        response = web.StreamResponse()
        response.headers['Content-Type'] = 'text/event-stream'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Connection'] = 'keep-alive'
        await response.prepare(request)

        async for chunk in generate_response(prompt):
            event_data = {
                'choices': [{
                    'delta': {'content': chunk},
                    'finish_reason': None,
                    'index': 0
                }]
            }
            await response.write(f'data: {json.dumps(event_data)}\n\n'.encode('utf-8'))

        # Send the final message
        await response.write(b'data: [DONE]\n\n')
        return response
    else:
        full_response = ''.join([chunk async for chunk in generate_response(prompt)])
        return web.json_response({
            'choices': [{
                'message': {'content': full_response},
                'finish_reason': 'stop',
                'index': 0
            }]
        })


app = web.Application()
app.router.add_post('/v1/chat/completions', chat_completions)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=11434)
