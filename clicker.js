function quickStepScrollToBottom(callback) {
  var currentPosition =
    window.pageYOffset ||
    document.documentElement.scrollTop ||
    document.body.scrollTop;
  var scrollStep = 50;

  function scrollStepLoop() {
    currentPosition += scrollStep;
    if (currentPosition >= document.body.scrollHeight - window.innerHeight) {
      window.scrollTo(0, document.body.scrollHeight);
      callback();
      return;
    }
    window.scrollTo(0, currentPosition);
    setTimeout(scrollStepLoop, 5);
  }

  scrollStepLoop();
}

function detailClicker() {
  document.querySelectorAll(".calendar__table tbody").forEach((bb) => {
    bb.querySelectorAll("td.calendar__detail a").forEach((l) => l.click());
  });
}

quickStepScrollToBottom(detailClicker);
