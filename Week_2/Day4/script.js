const inputTask = document.querySelector("#input-box");

const listContainer = document.querySelector("#list-container");
const addTaskBtn = document.querySelector(".addTaskBtn");

addTaskBtn.addEventListener("click", function (e) {
  addTask();
});

function addTask() {
  if (inputTask.value == "") {
    alert("Input field must be filled");
  } else {
    let li = document.createElement("li");
    li.innerHTML = inputTask.value;
    listContainer.appendChild(li);

    let span = document.createElement("span");
    span.innerHTML = "\u00d7";
    li.appendChild(span);
  }
  inputTask.value = "";
  saveData();
}

listContainer.addEventListener("click", function (e) {
  if (e.target.tagName === "LI") {
    e.target.classList.toggle("checked");
    saveData();
  } else if (e.target.tagName === "SPAN") {
    e.target.parentElement.remove();
    saveData();
  }
});

function saveData() {
  localStorage.setItem("data", listContainer.innerHTML);
}

function showTask() {
  listContainer.innerHTML = localStorage.getItem("data");
}

showTask();
