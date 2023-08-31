localStorage.clear();

function getTimestamps() {
  let timestamp_eventid_dict = {};

  window.calendarComponentStates[1].days.forEach((day) => {
    day.events.forEach((ev) => {
      timestamp_eventid_dict[`${ev.id}`] = {
        timestamp: ev.dateline * 1000,
        upnext: ev.upNext,
      };
    });
  });
  return timestamp_eventid_dict;
}

const timstamps = getTimestamps();
function extractCalendarSpecs(htmlContent) {
  let calendarSpecs = {};

  const specsTableRows = htmlContent
    .querySelector(".calendarspecs:last-child")
    .querySelectorAll("tr");

  specsTableRows.forEach((row) => {
    const key = row.querySelector("td:nth-child(1)").textContent.trim();
    const value = row.querySelector("td:nth-child(2)").textContent.trim();
    calendarSpecs[key] = value;
  });

  return calendarSpecs;
}

function extractCalendarHistory(htmlContent) {
  let calendarHistory = {};

  const historyTableRows = htmlContent.querySelectorAll(
    ".alternating.calendarhistory > tbody > tr:not(:first-child)"
  );

  historyTableRows.forEach((row, index) => {
    let history = "";
    let actual = "";
    let previous = "";
    let forecast = "";
    let actualtype = "";
    let previoustype = "";
    let revised = "";

    const historyElement = row.querySelector(
      "td.calendarhistory__row--history"
    );

    const actualElement = row.querySelector("td.calendarhistory__row--actual");
    const forecastElement = row.querySelector(
      "td.calendarhistory__row--forecast"
    );

    const previousElement = row.querySelector(
      "td.calendarhistory__row--previous"
    );

    if (historyElement) {
      history = historyElement.textContent.trim();
    }

    if (actualElement) {
      actual = actualElement.textContent.trim();
      actualtype = actualElement.children[0].className;
    }
    if (forecastElement) {
      forecast = forecastElement.textContent.trim();
    }
    if (previousElement) {
      previous = previousElement.textContent.trim();
      previoustype = previousElement.children[0].className
        .replace("revised", "")
        .trim();
      revised = previousElement.children[0].getAttribute("title") || "";
    }
    revised = revised.replace("Revised from ", "");
    const rowJson = {
      history,
      actual,
      actualtype,
      forecast,
      previous,
      previoustype,
      revised,
    };

    calendarHistory[index] = rowJson;
  });
  return calendarHistory;
}

function extractRelatedStories(htmlContent) {
  const relatedStories = {};
  const relatedStoriesTableRows = htmlContent.querySelectorAll(
    ".relatedstories > .flexposts > li.flexposts__story"
  );
  relatedStoriesTableRows.forEach((li, index) => {
    const json = {};
    const timestamp = li.dataset.timestamp;
    json.timestamp = timestamp;
    const aTag = li.querySelector("a");
    const href = aTag.getAttribute("href");
    const fullUrl = "www.forexfactory.com" + href;

    json.url = fullUrl;

    const title = aTag.getAttribute("title");
    json.title = title;

    const imgTag = li.querySelector(
      "div.flexposts__storydisplay-image > p > img"
    );
    const imgSrc = imgTag.getAttribute("src");
    json.img = imgSrc;

    const captionATag = li.querySelector("span.flexposts__caption > a");
    const captionHref = captionATag.getAttribute("href");
    const captionUrl = "www.forexfactory.com" + captionHref;
    const captionText = captionATag.innerText.substring(5).trim();
    json.from = {
      title: captionText,
      url: captionUrl,
    };

    const previewPTag = li.querySelector("p.flexposts__preview");
    const previewText = previewPTag.innerText.trim();
    json.preview = previewText;

    relatedStories[index] = json;
  });

  return relatedStories;
}

function extractRowData(htmlContent) {
  const eventid = htmlContent.getAttribute("data-event-id");

  const timestamp = parseInt(timstamps[eventid].timestamp);

  const currency = htmlContent
    .querySelector(".calendar__currency")
    .textContent.trim();
  const impact = htmlContent.querySelector(".calendar__impact span").title;
  const title = htmlContent
    .querySelector(".calendar__event-title")
    .textContent.trim();
  const actual = htmlContent
    .querySelector(".calendar__actual")
    .textContent.trim();
  const forecast = htmlContent
    .querySelector(".calendar__forecast")
    .textContent.trim();
  const previous = htmlContent
    .querySelector(".calendar__previous")
    .textContent.trim();

  const actualtype =
    htmlContent.querySelector(".calendar__actual").children[0].className;

  const previoustype = htmlContent
    .querySelector(".calendar__previous")
    .children[0].className.replace("revised", "")
    .trim();

  const revised =
    htmlContent
      .querySelector(".calendar__previous")
      .children[0].getAttribute("title") || "";

  const cov = new Date(timestamp);
  const date = cov
    .toLocaleString("en-US", {
      timeZone: "Asia/Tehran",
      weekday: "short",
      month: "short",
      day: "2-digit",
    })
    .replace(",", "");
  let time = cov
    .toLocaleString("en-US", {
      timeZone: "Asia/Tehran",
      hour: "numeric",
      minute: "numeric",
      hour12: true,
    })
    .replace(" ", "");
  const time_sure = htmlContent
    .querySelector(".calendar__time")
    .textContent.trim();

  if (
    !time_sure.includes("am") &&
    !time_sure.includes("pm") &&
    time_sure !== ""
  ) {
    time = time_sure;
  }

  const data = {
    timestamp: timestamp / 1000,
    eventid: eventid,
    date: date,
    time: time,
    currency: currency,
    impact: impact,
    title: title,
    actual: actual,
    forecast: forecast,
    previous: previous,
    actualtype: actualtype,
    previoustype: previoustype,
    revised: revised.replace("Revised from ", ""),
  };

  return data;
}

function findParentTd(element) {
  while (element && element.tagName !== "TD") {
    element = element.parentNode;
  }
  if (element === null || element === undefined) {
    return "notfound";
  } else if (element.classList.contains("calendar__cell")) {
    return element;
  } else {
    return "notfound";
  }
}

function findParentTr(element) {
  while (element && element.tagName !== "TR") {
    element = element.parentNode;
  }
  return element;
}

const body = document.body;

const observer = new MutationObserver((mutationsList) => {
  for (const mutation of mutationsList) {
    if (mutation.type === "childList") {
      for (const addedNode of mutation.addedNodes) {
        if (
          addedNode.nodeName === "TR" &&
          addedNode.classList.contains("calendar__details--detail")
        ) {
          const rowData = extractRowData(addedNode.previousElementSibling);
          const specs = extractCalendarSpecs(addedNode);
          const histories = extractCalendarHistory(addedNode);
          const related = extractRelatedStories(addedNode);
          const allRowData = {
            ...rowData,
            specs,
            histories,
            related,
          };
          localStorage.setItem(
            `rowData${allRowData.eventid}`,
            `${JSON.stringify(allRowData)}`
          );
        }

        if (findParentTd(mutation.target) !== "notfound") {
          const rowData = extractRowData(findParentTr(mutation.target));
          const specs = extractCalendarSpecs(
            findParentTr(mutation.target).nextElementSibling
          );
          const histories = extractCalendarHistory(
            findParentTr(mutation.target).nextElementSibling
          );
          const related = extractRelatedStories(
            findParentTr(mutation.target).nextElementSibling
          );
          const allRowData = {
            ...rowData,
            specs,
            histories,
            related,
          };
          localStorage.setItem(
            `rowData${allRowData.eventid}`,
            `${JSON.stringify(allRowData)}`
          );
        }
      }
    } else if (mutation.type === "characterData") {
      if (
        mutation.target.parentElement.classList.contains(
          "calendar__actual-wait"
        ) ||
        findParentTd(mutation.target) !== "notfound"
      ) {
        const rowData = extractRowData(findParentTr(mutation.target));
        const specs = extractCalendarSpecs(
          findParentTr(mutation.target).nextElementSibling
        );
        const histories = extractCalendarHistory(
          findParentTr(mutation.target).nextElementSibling
        );
        const related = extractRelatedStories(
          findParentTr(mutation.target).nextElementSibling
        );
        const allRowData = {
          ...rowData,
          specs,
          histories,
          related,
        };
        localStorage.setItem(
          `rowData${allRowData.eventid}`,
          `${JSON.stringify(allRowData)}`
        );
      }
    }
  }
});

observer.observe(body, {
  childList: true,
  characterData: true,
  subtree: true,
});
