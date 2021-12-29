function add_chatroom_to_item(data, item)
{
    var template = `
    <div class="card mt-2 chatroom-button" onclick="window.location.href='chatroom.html?id={id}'">
        <div class="card-body">
            <h5 class="card-title">{name}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{members}</h6>
        </div>
    </div>
    `;
    members = "";
    sep = ", ";
    for (member in data.members)
    {
        member = data.members[member]
        members += member.account.display_name + sep;
    }
    members = members.substring(0, members.length - 1 - sep.length);
    item.append(template_fill(template, {"name":data.name, "members":members, 'id':data.id}))
}

function update_chatrooms(data, item)
{
    item.empty()
    for (var i = 0; i < data.length; i++)
    {
        var chatroom = data[i];
        add_chatroom_to_item(chatroom, item);
    }
}

query_get("chatroom", (data) => {
    update_chatrooms(data, $("#chatrooms"))
})
