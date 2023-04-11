const submitBttn = document.getElementById("submitBttn");
submitBttn.disabled = true;

function cnfrmPsswd() {
  let p1 = document.getElementById("floatingPassword").value;
  let p2 = document.getElementById("floatingCnfrmPassword").value;
  
  if (p1 == p2) {
    document.getElementById("msg").innerHTML = "Passwords Match";
    submitBttn.disabled = false;
  } else {
    document.getElementById("msg").innerHTML = "Passwords Don't Match";
    submitBttn.disabled = true;
  }
}
