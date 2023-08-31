let found = 0;
for (let days = 0; days < calendarComponentStates[1].days.length; days++) {
  for (
    let events = 0;
    events < calendarComponentStates[1].days[days].events.length;
    events++
  ) {
    if (
      calendarComponentStates[1].days[days].events[events].greyed === false &&
      (calendarComponentStates[1].days[days].events[events].timeLabel.includes(
        "am"
      ) ||
        calendarComponentStates[1].days[days].events[events].timeLabel.includes(
          "pm"
        ))
    ) {
      found = calendarComponentStates[1].days[days].events[events].dateline;
      break;
    }
  }
  if (found !== 0) {
    break;
  }
}

return found;
