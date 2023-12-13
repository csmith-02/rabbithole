
const addCommentBtn = document.querySelector("#add")
const addCommentSection = document.querySelector('#comment')
const cancelBtn = document.querySelector('#cancel')
let inputField = document.querySelector('#inputField')

addCommentBtn.addEventListener('click', () => {
    if (!addCommentSection.classList.contains('hidden')) {
        // do nothing the user can already type in a comment
    } else {
        addCommentSection.classList.remove('hidden')
        inputField.focus()
    }
})

cancelBtn.addEventListener('click', () => {
    addCommentSection.classList.add('hidden')
})