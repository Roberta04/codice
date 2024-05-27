css = '''
<style>

.chat-container {
    flex: 1;
    display: flex;
    flex-direction: column-reverse;
    overflow-y: auto;
    padding: 1rem;
    background-color: #1a1a1a;
}


.chat-input-container {
    padding: 1rem;
    background-color: #2b313e;
    position: fixed;
    bottom: 0;
    width: 100%;
}

.chat-message {
    padding: 1rem 2.0rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    display: flex;
    max-width: 100%;
    word-wrap: break-word;
    
}
.chat-message.user {
    background-color: #E08D67;
    justify-content:flex-end;
    border-bottom-right-radius:0;
    align-items:center;
    
}
.chat-message.bot {
    background-color: #EFB983;
    justify-content:flex-start;
    border-bottom-left-radius:0;
    align: start
}
.chat-message .avatar {
margin-right:2rem;

}
.chat-message .user.avatar {
    order: 2;
    
}
.chat-message .bot.avatar {
    order: 1;
    
}

.chat-message .avatar img {
max-width: 78px;
max-height: 78px;
border-radius: 50%;
object-fit: cover;

}
.chat-message .message {

color: #4A2713;
}
.chat-message .user.message {
    order: 1;
    text-align: right;
    
    
}
.chat-message .bot.message {
    order: 2;
    text-align: left;
    
    
}

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/yPtQDkn/download.png"max-height: 78px; max-width:  78px; border-radius: 90%; object-fit: cover ;></a>
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
</div>
'''