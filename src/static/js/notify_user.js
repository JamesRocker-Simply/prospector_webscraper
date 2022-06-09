function event_log_to_notification_area(base_url) {
    const node = document.createElement("LI");
    const text_node = document.createTextNode(`${base_url} has been searched`);
    node.appendChild(text_node);
    document.getElementById("notification_area").appendChild(node);
}


function add_loading_gif() {
    const node = document.createElement("LI");
    const img = document.createElement("img");
    img.src = "https://c.tenor.com/wpSo-8CrXqUAAAAi/loading-loading-forever.gif";
    node.appendChild(img)

    document.getElementById("loading").appendChild(node);
}