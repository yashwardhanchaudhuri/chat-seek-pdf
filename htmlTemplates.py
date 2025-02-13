css = '''
<style>
.chat-message {
    padding: 1.2rem;
    border-radius: 1.2rem;
    margin-bottom: 1rem;
    display: flex;
    max-width: 80%;
    margin-left: auto;
    margin-right: auto;
    transition: all 0.3s ease;
}

.chat-message.user {
    background-color: #007AFF;
    margin-left: auto;
}

.chat-message.bot {
    background-color: #E9E9EB;
    margin-right: auto;
}

.chat-message .avatar {
    width: 15%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
}

.chat-message.user .avatar {
    color: #FFFFFF;
}

.chat-message.bot .avatar {
    color: #000000;
}

.chat-message .message {
    width: 85%;
    padding: 0 1rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 0.95rem;
    line-height: 1.4;
}

.chat-message.user .message {
    color: #FFFFFF;
}

.chat-message.bot .message {
    color: #000000;
}

@media (max-width: 768px) {
    .chat-message {
        max-width: 90%;
    }
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">Deepseek</div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">User</div>
    <div class="message">{{MSG}}</div>
</div>
'''
