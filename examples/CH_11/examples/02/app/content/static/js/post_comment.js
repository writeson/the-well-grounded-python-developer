/**
 * Handle the page comment button and use it
 * to put the put the post_uid value into the
 * create comment form's parent_post_uid field
 */
const buttons = document.getElementsByClassName('post-comment')
for (const button of buttons) {
  button.addEventListener('click', (e) => {
    const post_uid = e.target.dataset.postUid;
    document.getElementById('parent_post_uid').value = post_uid;
  })
}
/**
 * Set the focus on text area in the modal
 */
const commentModal = document.getElementById('comment_modal');
commentModal.addEventListener('shown.bs.modal', () => {
  document.getElementById("comment").focus();
})
