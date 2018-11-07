function report() {
    alert("Thank you for your feedback!");
  }

function changeColor(obj, correctness) {
//    var target = e.target;
    if (correctness == "v") {
        obj.style.backgroundColor = '#007216';
    } else if (correctness == "x") {
        obj.style.backgroundColor = '#05701e';
    }
}