import os
import requests

TOKEN = os.environ['TOKEN']
CHAT_ID = -1001621175874


def format_message(message):
    (post_id, title, text, images) = message

    return f'''
*{title}*


```
{text.strip()}
``` 

https://www.ivanovonews.ru/news/{post_id}/
    '''.strip()


def send(message):
    (post_id, title, text, images) = message

    return send_as_image(message) if images else send_as_text(message)


def send_as_text(message):
    SEND_API = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    (post_id, title, text, images) = message

    response = requests.post(
        url=SEND_API,
        json={
            'chat_id': CHAT_ID,
            'text': format_message(message),
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True,
            # 'reply_markup': {
            #     'inline_keyboard': [
            #         [{'text': 'Nice', 'callback_data': '+'}, {'text': 'Unnice', 'callback_data': '-'}],
            #     ]
            # }
        }
    )

    if response.ok:
        mark_as_sent(post_id)


def send_as_image(message):
    SEND_API = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'

    (post_id, title, text, images) = message
    if len(images) > 1:
        return send_as_image_group(message)

    response = requests.post(
        url=SEND_API,
        json={
            'chat_id': CHAT_ID,
            'photo': f'https://www.ivanovonews.ru{images[0]}',
            'caption': format_message(message),
            'parse_mode': 'Markdown',
        }
    )

    if response.ok:
        mark_as_sent(post_id)


def send_as_image_group(message):
    SEND_API = f'https://api.telegram.org/bot{TOKEN}/sendMediaGroup'

    (post_id, title, text, images) = message

    media = [{
        'type': 'photo',
        'media': f'https://www.ivanovonews.ru{url}'} for url in images]
    media[0]['parse_mode'] = 'Markdown'
    media[0]['caption'] = format_message(message)

    response = requests.post(
        url=SEND_API,
        json={
            'chat_id': CHAT_ID,
            'media': media,
        }
    )

    if response.ok:
        mark_as_sent(post_id)


def mark_as_sent(post_id):
    with open('data/position', 'w+') as position:
        position.write(str(post_id))
    print(f'{post_id} commited!')
