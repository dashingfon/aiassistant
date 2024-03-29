let disableButtons = () => {
  document.querySelectorAll("button").forEach((button) => {
    button.disabled = true;
  });
};

let enableButtons = () => {
  document.querySelectorAll("button").forEach((button) => {
    button.disabled = false;
  });
};

let send_to_backend = async (message) => {
  let response = await fetch(`/get_response?message=${message}`, {
    method: "GET"
  })
  response_json = await response.json()
  return response_json.response
}

let is_hidden = (element) => {
  if (element.classList.contains("hidden")) {
    return true
  } else {
    return false
  }
}

htmx.logger = (elt, event, data) => {
  if (console) {
    console.log(event, elt, data);
  }
};


document.getElementById("send-button").addEventListener("click", async () => {
  disableButtons()
  if (!is_hidden(document.getElementById("default-chat"))) {
    document.getElementById("chats").classList.remove("hidden")
    document.getElementById("default-chat").classList.add("hidden")
  }
  let input_element = document.getElementById("chat-input")
  let message = input_element.innerHTML
  input_element.innerHTML = "";
  let human_message_string = human_message(`<div class="chat-content">${message}</div>`)
  let ai_message_string = ai_message('<div class="chat-content pending"><img src="/media/Circles-menu-3.gif" alt="awaiting response"></div>')
  let chat = document.getElementById("chats")
  chat.insertAdjacentHTML("beforeend", human_message_string)
  chat.insertAdjacentHTML("beforeend", ai_message_string)
  let chat_area = document.getElementById("chats-area")
  chat_area.scrollTop = chat_area.scrollHeight
  let ai_response = await send_to_backend(message)
  let ai_response_element = document.querySelector('.pending')
  ai_response_element.classList.remove("pending")
  ai_response_element.innerHTML = ai_response
  enableButtons()
})

document.getElementById("clear-chats").addEventListener("click", () => {
  document.getElementById("chats").classList.add("hidden")
  document.getElementById("default-chat").classList.remove("hidden")
})
