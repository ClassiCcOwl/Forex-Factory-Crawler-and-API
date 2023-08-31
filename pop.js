function pop() {
  const values = Object.values(localStorage);
  localStorage.clear();
  return values;
}
return pop();
