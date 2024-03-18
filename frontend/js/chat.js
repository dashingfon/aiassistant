htmx.logger = (elt, event, data) => {
    if (console) {
      console.log(event, elt, data);
    }
  };

let disableButtons = () => {}

let enableButtons = () => {}

document.getElementById("send-button").addEventListener("click", () => {
    // if default hide default
    // first add message to element
    // then send to backend
    // then add waiting gif
})
