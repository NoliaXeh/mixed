function add_message_to_item(data, item)
{
    var template = `
    <div class="message {class}" id="message-{id}">
        <img src="{image}" class=""/>
        <div class="card" id="message-body-{id}">
            <h6 class="card-subtitle m-2 text-muted">{author}</h6>
            <div class="card-body mt-0 pt-0">
                {body}
            </div>
            <h6 class="card-subtitle text-muted date">{date}</h6>
        </div>
    </div>
    `;
    
    var author = "unknown";
    var style = "message-left";
    var date = format_date(data.created_at)
    var image = "https://via.placeholder.com/128";
    var id = data.id;
    if (data.author)
    {
        if (data.author.alter)
            author = data.author.alter.name
        else if (data.author.account)
            author = data.author.account.display_name
        
        if (data.author.account.id == current_chatroom.members[0].account.id)
            style = "message-right";
        image = data.author.account.profile_picture;
        if (data.author.alter !== null)
        {
            image = data.author.alter.profile_picture;
        }
    }
    var obj = template_fill(template, {
        "body":data.body,
        "author":author,
        "class": style,
        "date":date,
        "image": image,
        "id": id,
    })
    item.append(obj)
    obj = $("#message-"+id);
    console.log(obj.width());
    var body = $("#message-body-"+id);
    if (body.width() >= obj.width() * 0.9)
    {
        $("#message-"+id+" img").addClass("ontop");
        obj.addClass("w-100 m-0");
        obj.css("position", "relative");
        obj.css("top", "-0.5em");


    }

}

function update_message(data, item)
{
    item.empty()
    for (var i = 0; i < data.length; i++)
    {
        var chatroom = data[i];
        add_message_to_item(chatroom, item);
    }
    scroll_down();
}

function send_message() {
    var message_content = document.getElementById("message-in").value;
    var author_id = parseInt(document.getElementById("author-select").value);
    query_post("message/", (data) =>
    {
        query_get("get_message/" + data.id + "/", (data) => {
            add_message_to_item(data, $("#messages"));
            scroll_down();
        });
        document.getElementById("message-in").value = "";
    },
    {
        chatroom: current_chatroom.id,
        author: author_id,
        body: message_content,
    })
}

function go_back()
{
    window.location.href = 'index.html';
}

function update_authors() {
    var accounts = "";
    for (var i = 0; i < current_chatroom.members.length; i++)
    {
        member = current_chatroom.members[i];
        accounts += member.account.id;
        if (i < current_chatroom.members.length - 1)
            accounts += ",";
    }
    query_get("get_people/?accounts=" + accounts, (data) => {
        var template = `
        <option value="{id}">{name}</option>
        `;
        var select = "";
        for (i in data)
        {
            people = data[i];
            console.log(people);
            var name = people.account.display_name;
            if (people.alter !== null)
                name = people.alter.name;
            select += template_fill(template, {"id": people.id, "name": name})
        }
        $("#author-select").append(select)
    })
}


let current_chatroom = null;
var _GET=[];
window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,function(a,name,value){_GET[name]=value;});

var chatroom_url = "chatroom/" + _GET["id"];
query_get(chatroom_url, (data) => {
    current_chatroom = data;
    set_chatroom_title();
    init_messages();
    update_authors();
});

function init_messages()
{
    var get_message_url = "get_message/?chatroom=" + current_chatroom.id
    query_get(get_message_url,(data) => {
        update_message(data, $("#messages"))
    });   
}

function set_chatroom_title()
{
    template = `
        <h2>
            {title}
        </h2>
    `;
    $("#chatroom_title").append(template_fill(template, {
        "title": current_chatroom.name,
    }));

}

document.body.addEventListener('keypress', (e) => {
    if (e.key == "Enter")
    {
        send_message();
    }
});