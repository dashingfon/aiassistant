htmx.logger = (elt, event, data) => {
    if (console) {
      console.log(event, elt, data);
    }
  };

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
  let response = await fetch(`/get_response?messsage=${message}`, {
    method: "GET"
  })
  return response
}


document.getElementById("send-button").addEventListener("click", async () => {
  if (default_message) {
    document.getElementById("chats").classList.remove("hidden")
    document.getElementById("default-chat").classList.add("hidden")
  }
  let imput_element = document.getElementById("chat-input")
  let message = imput_element.innerHTML
  imput_element.innerHTML = "";
  disableButtons()
  let human_message = human_message(message)
  let ai_message = ai_message('<img src="/media/Circles-menu-3.gif" alt="">')
  document.getElementById("chats").insertAdjacentHTML("afterend", human_message)
  document.getElementById("chats").insertAdjacentHTML("afterend", ai_message)
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
