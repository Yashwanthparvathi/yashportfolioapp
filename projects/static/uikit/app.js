// Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
//   hljs.highlightAll();
// });


// document.addEventListener('DOMContentLoaded', function () {
//   hljs.highlightAll();
// });


// let alertWrapper = document.querySelector('.alert')
// let alertClose = document.querySelector('.alert__close')

// if (alertWrapper) {
//   alertClose.addEventListener('click', () =>
//     alertWrapper.style.display = 'none'
//   )
// }
function closeAlert(button) {
  button.parentElement.style.display = 'none';
}