
let editBtns = document.querySelectorAll('.edit')
let body = document.getElementById('body')
let domBody = document.getElementsByTagName('body').item(0)
let domModal = document.getElementById('modal')
let nav = document.getElementsByTagName('nav').item(0)

// Buttons that will have to be disabled upon modal appearing
let home = document.getElementById('home')
let community = document.getElementById('community')
let profile = document.getElementById('profile')
let addPost = document.getElementById('addPost')
let allDeleteBtns = document.querySelectorAll('.delete') 

editBtns.forEach(editBtn => {
    editBtn.addEventListener('click', (e) => {
        e.preventDefault()
        if (domModal) {
            // do nothing, the modal is already up
        } else {

            let postCommunity = editBtn.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.firstElementChild.children.item(1).firstElementChild.textContent
            let postTitle = editBtn.parentElement.parentElement.parentElement.parentElement.parentElement.firstElementChild.firstElementChild.firstElementChild.textContent
            let postContent = editBtn.parentElement.parentElement.parentElement.parentElement.previousElementSibling.textContent
            let editform = (editBtn.parentElement).action
            let modal = createModal(postCommunity, postTitle, postContent, editform)
            
            domBody.classList.add('modal-open')
            body.classList.add('overlay')
            nav.classList.add('overlay')
            domBody.insertBefore(modal, body)

            editBtn.disabled = true
            
            addPost.disabled = true

            allDeleteBtns.forEach(btn => {
                btn.disabled = true
            })

            let cancel = document.getElementById('cancel')
    
            cancel.addEventListener('click', event1 => {
                event1.preventDefault()
    
                domBody.classList.remove('modal-open')
                body.classList.remove('overlay')
                nav.classList.remove('overlay')
                domBody.removeChild(modal)

                allDeleteBtns.forEach(btn => {
                    btn.disabled = false
                })

                addPost.disabled = false

                editBtns.forEach(btn => {
                    btn.disabled = false
                })
            })

            let typedTitle = document.getElementById('title')
            let typedContent = document.getElementById('content')
            let cform = document.querySelector('#c-form')
            typedTitle.addEventListener('keyup', () => {
                currentTitle = typedTitle.value
                currentContent = typedContent.value
                if (currentTitle == '' || currentContent == '') {
                    if (!(cform.children.length >= 5)) {
                        let error = document.createElement('p')
                        error.textContent = 'Title or Content cannot be blank.'
                        cform.appendChild(error)
                        error.classList.add('text-danger')
                        error.classList.add('text-center')
                        error.classList.add('mt-5')
                    }
                } else {
                    if (cform.children.length >= 5) {
                        lastChild = cform.children.item(4)
                        cform.removeChild(lastChild)
                    }
                }
            })
            typedContent.addEventListener('keyup', () => {
                currentContent = typedContent.value
                currentTitle = typedTitle.value
                if (currentContent == '' || currentTitle == '') {
                    if (!(cform.children.length >= 5)) {
                        let error = document.createElement('p')
                        error.textContent = 'Title or Content cannot be blank.'
                        cform.appendChild(error)
                        error.classList.add('text-danger')
                        error.classList.add('text-center')
                        error.classList.add('mt-5')
                    }
                } else {
                    if (cform.children.length >= 5) {
                        lastChild = cform.children.item(4)
                        cform.removeChild(lastChild)
                    }
                }
            })
        } 
    })
})

function createModal(postCommunity, postTitle, postContent, editform) {
    // Create Containers
    let modal = document.createElement('div')
    let formContainer = document.createElement('div')
    let form = document.createElement('form')
    let communityDiv = document.createElement('div')
    let communityLabel = document.createElement('label')
    let communityInput = document.createElement('input')
    let hiddenComInput = document.createElement('input')
    let titleDiv = document.createElement('div')
    let titleLabel = document.createElement('label')
    let titleInput = document.createElement('input')
    let contentDiv = document.createElement('div')
    let contentLabel = document.createElement('label')
    let contentTextArea = document.createElement('textarea')
    let saveChangesDiv = document.createElement('div')
    let saveChangesBtn = document.createElement('button')
    let cancelBtn = document.createElement('button')

    // Customize containers
    communityDiv.classList.add('d-flex')
    communityDiv.classList.add('mb-3')
    communityLabel.classList.add('h3')
    communityLabel.classList.add('mr-3')
    communityLabel.setAttribute('for', 'community')
    communityLabel.textContent = 'Community: '
    communityInput.classList.add('form-control')
    communityInput.type = 'text'
    communityInput.name = 'community-show'
    communityInput.id = 'community-show'
    communityInput.value = postCommunity
    communityInput.disabled = true
    hiddenComInput.type = 'hidden'
    hiddenComInput.name = 'community'
    hiddenComInput.value = postCommunity
    titleDiv.classList.add('d-flex')
    titleDiv.classList.add('mb-3')
    titleLabel.setAttribute('for', 'title')
    titleLabel.classList.add('h3')
    titleLabel.classList.add('mr-3')
    titleLabel.textContent = 'Title: '
    titleInput.type = 'text'
    titleInput.id = 'title'
    titleInput.name = 'title'
    titleInput.classList.add('form-control')
    titleInput.value = postTitle
    contentDiv.classList.add('c-div')
    contentDiv.classList.add('d-flex')
    contentDiv.classList.add('mb-5')
    contentLabel.setAttribute('for', 'content')
    contentLabel.classList.add('h3')
    contentLabel.classList.add('mr-3')
    contentLabel.textContent = 'Content: '
    contentTextArea.classList.add('form-control')
    contentTextArea.id = 'content'
    contentTextArea.name = 'content'
    contentTextArea.textContent = postContent
    saveChangesDiv.classList.add('text-center')
    saveChangesBtn.classList.add('btn')
    saveChangesBtn.classList.add('mr-2')
    saveChangesBtn.classList.add('btn-primary')
    saveChangesBtn.type = 'submit'
    saveChangesBtn.textContent = 'Save Changes'
    cancelBtn.textContent = 'Cancel'
    cancelBtn.id = 'cancel'
    cancelBtn.classList.add('btn')
    cancelBtn.classList.add('btn-danger')

    form.action = editform
    form.method = 'post'
    form.id = 'c-form'
    formContainer.classList.add('p-5')
    modal.id = 'modal'
    modal.classList.add('position-fixed')
    modal.classList.add('border')
    modal.classList.add('border-dark')
    modal.classList.add('rounded')
    modal.classList.add('rounded-2')

    // Append All containers together
    communityDiv.appendChild(communityLabel)
    communityDiv.appendChild(communityInput)
    communityDiv.appendChild(hiddenComInput)
    titleDiv.appendChild(titleLabel)
    titleDiv.appendChild(titleInput)
    contentDiv.appendChild(contentLabel)
    contentDiv.appendChild(contentTextArea)
    saveChangesDiv.appendChild(saveChangesBtn)
    saveChangesDiv.appendChild(cancelBtn)

    form.appendChild(communityDiv)
    form.appendChild(titleDiv)
    form.appendChild(contentDiv)
    form.appendChild(saveChangesDiv)

    formContainer.appendChild(form)

    modal.appendChild(formContainer)
    return modal
}