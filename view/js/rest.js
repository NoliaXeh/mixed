
// let APIRootURL = "http://127.0.0.1:8000/"
let APIRootURL = "http://127.0.0.1:8000/"

function setAPIRootURL (root)
{
    APIRootURL = root;
}

function combineURL (...urls)
{
    left = urls[0]
    for (var i = 1; i < urls.length; i++)
    {
        right = urls[i];
        if (left[left.length - 1] != "/")
            left += "/"
        if (right[0] == "/")
            right = right.substring(1)
        left += right
    }
    // if (left[-1] != "/")
    //     left += "/"
    return left
}

function query_get (url, then, param = null, success = null, fail = null)
{
    if (!url.includes(APIRootURL))
        url = combineURL(APIRootURL, url)
    if (success == null) success = () => {};
    if (fail    == null) fail    = () => {};
    $.get(url, param, then, "json")
    .done(success)
    .fail(fail)
    .always(()=>{})
}

function query_post (url, then, param = null, success = null, fail = null)
{
    if (!url.includes(APIRootURL))
        url = combineURL(APIRootURL, url)
    if (success == null) success = () => {};
    if (fail    == null) fail    = () => {};
    $.post(url, param, then, "json")
    .done(success)
    .fail(fail)
    .always((data)=>{
        console.log(data);
    })
}

function template_fill(template, vars)
{
    for (key in vars)
    {
        value = vars[key];
        template = template.replaceAll("{"+key+"}", value)
    }
    return template;
}

const LANG = "fr-FR"

function translate(mot, lang)
{
    var t = {
        "today": {
            "fr-FR": "aujourd'hui",
            "en-US": "today"
        },
        "yesterday": {
            "fr-FR": "hier",
            "en-US": "yesterday"
        },
        "create a room": {
            "fr-FR": "créer un salon",
            "en-US": "create a room",
        },
        "name of the room": {
            "fr-FR": "nom du salon",
            "en-US": "name of the room",
        }
    };
    if (mot in t)
        if (LANG in t[mot])
            return t[mot][LANG];
        else
            return mot;
    else
        return mot;
}

function format_date(raw_date)
{
    var date = new Date(raw_date);
    var now = new Date();
    var diff = now - date; // in millis
    var months = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    var formated_date = date.toLocaleDateString(LANG) + ", " + date.toLocaleTimeString(LANG);
    if (date.getDate() == now.getDate() - 1 && date.getMonth() == now.getMonth() && date.getFullYear() == now.getFullYear() 
        || now.getDate() == 1 && date.getDate() == months[date.getMonth()] && date.getMonth() == now.getMonth() - 1
        )
    {
        formated_date = translate("yesterday", LANG) + ", " + date.toLocaleTimeString(LANG);
    }
    else if (date.getDate() == now.getDate() && date.getMonth() == now.getMonth() && date.getFullYear() == now.getFullYear())
    {
        formated_date = date.toLocaleTimeString(LANG);
    }
    return formated_date;

}

function scroll_down(){
    window.scrollTo(0,document.body.scrollHeight);
}