//switch button1
const toggleSwitch1 = document.getElementById("switch1");
const toggleStatus1 = document.getElementById("switch-status1");

function onCheckboxToggle1() {
  const isChecked1 = this.hasAttribute("checked");

  /* 1. Update toggle switch visual state. */
  this.toggleAttribute("checked");

  /* 2. Update toggle switch status text. */
  toggleStatus1.innerText = isChecked1 ? "OFF" : "ON";
  console.log("switch 1 =", !isChecked1); /* status switch1 */
}
toggleSwitch1.addEventListener("change", onCheckboxToggle1);

//switch button2
const toggleSwitch2 = document.getElementById("switch2");
const toggleStatus2 = document.getElementById("switch-status2");

function onCheckboxToggle2() {
  const isChecked2 = this.hasAttribute("checked");

  /* 1. Update toggle switch visual state. */
  this.toggleAttribute("checked");

  /* 2. Update toggle switch status text. */
  toggleStatus2.innerText = isChecked2 ? "OFF" : "ON";

  console.log("switch 2 =", !isChecked2); /* status switch2 */
}

toggleSwitch2.addEventListener("change", onCheckboxToggle2);
