function add_chatroom_to_item(data, item)
{
    var template = `
    <div class="card mt-2 chatroom-button" onclick="window.location.href='chatroom.html?id={id}'">
        <div class="card-body">
            <div class="card-title d-flex m-0"> <span class="me-2">{name}</span> {members}</div>
        </div>
    </div>
    `;
    members = "<div>";
    sep = ", ";
    var pp_template = '<img src="{img}" class="pp_round" />'
    for (member in data.members)
    {
        member = data.members[member]
        console.log(member)
        members += template_fill(pp_template, {"img": member.account.profile_picture});
    }
    members += "</div>";
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

function create_chatroom_form()
{
    var template = `
    <div id="blur" class="chat-room-form-element"></div>
    <div class="card chat-room-form-element" id="create_a_room_form">
        <div class="card-header text-capitalize ">
            <div class="row">
                <div class="col-11" style="position: relative; top: 8px" >
                    {create_a_room}
                </div>
                <div class="col-1">
                    <button type="button" class="btn" style="position: relative; left: -32px" onclick="close_chatroom_form()" ontouch="close_chatroom_form()">
                        <svg xmlns="http://www.w3.org/2000/svg"  width="24" height="24" fill="currentColor" class="bi bi-x-square" viewBox="0 0 16 16">
                            <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
                            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="input-group mb-3">
                <input type="text" class="form-control" id="chatroom-form-name" placeholder="{name_of_chatroom}" aria-describedby="chatroom-form-validate">
                <button class="btn btn-outline-secondary" type="button" id="chatroom-form-validate" onclick="create_chatroom_by_form()" ontouch="create_chatroom_by_form()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
                        <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>
    `;
    var final_html = template_fill(template, {
        "create_a_room": translate("create a room", LANG),
        "name_of_chatroom": translate("name of the room", LANG),
    })
    $("body").append(final_html);
}

function create_chatroom_by_form() {
    var name = document.getElementById("chatroom-form-name").value;
    if (name == "") return;
    console.log(name);
    query_post("chatroom/", (data) => {
        console.log(data);
        close_chatroom_form();
    },
    {
        name: name
    })
}

function close_chatroom_form()
{
    $(".chat-room-form-element").remove();
}

query_get("chatroom", (data) => {
    update_chatrooms(data, $("#chatrooms"))
})