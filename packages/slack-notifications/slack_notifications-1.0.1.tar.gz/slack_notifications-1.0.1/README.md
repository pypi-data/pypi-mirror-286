# Slack notifications

## Installation

```bash
pip install slack-notifications
```


## Simple usage

```python
import os

import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


slack.send_notify('channel-name', username='Bot', text='@channel This is test message')
```

or

```python
import os

from slack_notifications import Slack


slack = Slack('<token>')
slack.send_notify('channel-name', username='Bot', text='@channel This is test message')
```

## Message

```python
import os

from slack_notifications import Slack, Attachment


slack = Slack('<token>')
message = slack.send_notify('channel-name', username='Bot', text='@channel This is test message')

message.text = 'This is test message'
message.update()

message.add_reaction('<name>')
message.remove_reaction('<name>')

message.upload_file('./test.yml', filetype='yaml')

message.attachments.append(
    Attachment(
        title='Attachment title',
        pretext='Attachment pretext',
        text='Attachment text',
        footer='Attachment footer',
        color='green',
    ),
)
message.update()
```

## Use attachments

```python
import os

import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


attachment = slack.Attachment(
    title='Attachment title',
    pretext='Attachment pretext',
    text='Attachment text',
    footer='Attachment footer',
    color='green',
)

slack.send_notify('channel-name', username='Bot', text='@channel This is test message', attachments=[attachment])
```

See program API


## Attachment fields

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


attachment = slack.Attachment(
    title='Attachment title',
    pretext='Attachment pretext',
    text='Attachment text',
    footer='Attachment footer',
    fields=[
        slack.Attachment.Field(
            title='Field title',
            value='Field value',
        ),
    ],
    color='green',
)

slack.send_notify('channel-name', username='Bot', text='@channel This is test message', attachments=[attachment])
```


## Simple Text Block

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


block = slack.SimpleTextBlock(
    'Text example',
    fields=[
        slack.SimpleTextBlock.Field(
            'Text field',
        ),
        slack.SimpleTextBlock.Field(
            'Text field',
            emoji=True,
        ),
    ],
)

slack.send_notify('channel-name', username='Bot', text='@channel This is test message', blocks=[block])
```

## Action Block

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


block = slack.ActionsBlock(
    elements=[
        slack.ButtonBlock(
            'Yes', 
            action_id='action1',
            value='some_data1',
            style='primary'
        ),
        slack.ButtonBlock(
            'No', 
            action_id='action2',
            value='some_data2',
            style='danger'
        ),
    ],
)

slack.send_notify('channel-name', username='Bot', text='@channel This is test message', blocks=[block])
```


## Use mrkdwn module

```python
import slack_notifications as slack


block = slack.SimpleTextBlock(
    'Text example',
    fields=[
        slack.SimpleTextBlock.Field(
            slack.mrkdwn.bold('Text field'),
        ),
        slack.SimpleTextBlock.Field(
            slack.mrkdwn.italic('Text field'),
            emoji=True,
        ),
    ],
)
```

## Mattermost interface

### Simple usage

```python
import os

import slack_notifications.mattermost as mattermost


mattermost.ACCESS_TOKEN = 'xxx'
mattermost.BASE_URL_ENV_NAME = 'http://your-mattermost-url.com/api/v4'
mattermost.TEAM_ID_ENV_NAME = 'xxx'

mattermost.send_notify('channel-name', username='Bot', text='@channel This is test message')
```

or

```python
import os

from slack_notifications.mattermost import Mattermost


mattermost = Mattermost('http://your-mattermost-url.com/api/v4',
                   token='<token>',
                   team_id='xxx')
mattermost.send_notify('channel-name', username='Bot', text='@channel This is test message')
```


### Use fields for Mattermost

```python
import slack_notifications.mattermost as mattermost
import slack_notifications as slack


mattermost.ACCESS_TOKEN = 'xxx'
mattermost.BASE_URL = 'http://your-mattermost-url.com/api/v4'
mattermost.TEAM_ID = 'xxx'


block = slack.SimpleTextBlock(
    'Text example',
    fields=[
        slack.SimpleTextBlock.Field(
            'Text field',
        ),
        slack.SimpleTextBlock.Field(
            'Text field',
            emoji=True,
        ),
    ],
)

mattermost.send_notify('channel-name', username='Bot', text='@channel This is test message', blocks=[block])
```


### Use mrkdwn module for Mattermost

```python
import slack_notifications as slack
from slack_notifications.mattermost import mrkdwn


block = slack.SimpleTextBlock(
    'Text example',
    fields=[
        slack.SimpleTextBlock.Field(
            mrkdwn.bold('Text field'),
        ),
        slack.SimpleTextBlock.Field(
            mrkdwn.italic('Text field'),
            emoji=True,
        ),
    ],
)
```
See program API

## Init color

```python
import slack_notifications as slack


slack.init_color('green', '#008000')
```


## Call slack resource

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


response = slack.call_resource(slack.Resource('users.info', 'GET'), params={'user': 'W1234567890'})
```


## Resource iterator

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


for user in slack.resource_iterator(slack.Resource('users.list', 'GET'), 'members'):
    pass
```


## Raise exception if error was given

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


slack.send_notify('channel-name', username='Bot', text='@channel This is test message', raise_exc=True)
```


# Program API

## send_notify

* channel
* text: str = None
* username: str = None
* icon_url: str = None
* icon_emoji: str = None
* link_names: bool = True
* raise_exc: bool = False
* attachments: List[Attachment] = None
* blocks: List[BaseBlock] = None

## upload_file

* channel
* file
* title: str = None,
* content: str = None,
* filename: str = None,
* thread_ts: str = None,
* filetype: str = 'text',
* raise_exc: bool = False

## call_resource

* resource: Resource
* raise_exc: bool = False
* **kwargs (requests lib options)


## resource_iterator

* resource: Resource
* from_key: str
* cursor: str = None
* raise_exc: bool = False
* limit: int = DEFAULT_RECORDS_LIMIT


## init_color

* name: str
* code: str


## Attachment

* image_url: str = None,
* thumb_url: str = None,
* author_name: str = None,
* author_link: str = None,
* author_icon: str = None,
* title: str = None,
* title_link: str = None,
* text: str = None,
* pretext: str = None,
* footer: str = None,
* footer_icon: str = None,
* timestamp: str = None,
* fields: List[Attachment.Field] = None,
* color: str = None

### Attachment.Field

* title: str = None
* value: str = None
* short: bool = False


## SimpleTextBlock

* text: str
* mrkdwn: bool = True
* block_id: str = None
* fields: List[SimpleTextBlock.Field] = None

### SimpleTextBlock.Field

* text: str
* emoji: bool = False
* mrkdwn: bool = True


## DividerBlock

* block_id: str = None


## ImageBlock

* image_url: str
* title: str = None
* alt_text: str = None
* mrkdwn: bool = True
* block_id: str = None


## ContextBlock

* elements: List[Union[ContextBlock.TextElement, ContextBlock.ImageElement]]
* block_id: str = None

### ContextBlock.TextElement

* text: str
* mrkdwn: bool = True

### ContextBlock.ImageElement

* image_url: str
* alt_text: str = None


## ActionsBlock
* elements: List[ButtonBlock]

### ButtonBlock
* text: str
* action_id: str
* value: str
* style: str = None
