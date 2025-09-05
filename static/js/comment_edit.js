document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-comment-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const commentDiv = btn.closest('.comment');
            const editForm = commentDiv.querySelector('.comment-edit-form');

            // Скрываем кнопку "Изменить"
            btn.style.display = 'none';

            // Показываем форму редактирования
            editForm.style.display = 'block';

            const cancelBtn = editForm.querySelector('.cancel-edit-btn');
            const saveBtn = editForm.querySelector('.save-edit-btn');
            const textarea = editForm.querySelector('.edit-content');

            // Отмена
            cancelBtn.addEventListener('click', () => {
                editForm.style.display = 'none';
                btn.style.display = 'inline-block';
                textarea.value = commentDiv.querySelector('.comment-content').textContent.trim();
            });

            // Сохранение
            saveBtn.addEventListener('click', () => {
                const url = saveBtn.getAttribute('data-url');
                const data = new FormData();
                data.append('content', textarea.value);

                fetch(url, {
                    method: 'POST',
                    body: data,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (response.ok) {
                        commentDiv.querySelector('.comment-content').textContent = textarea.value;
                        editForm.style.display = 'none';
                        btn.style.display = 'inline-block';
                    } else if (response.status === 403) {
                        alert('Вы не можете редактировать чужой комментарий!');
                        editForm.style.display = 'none';
                        btn.style.display = 'inline-block';
                    } else {
                        alert('Ошибка при сохранении комментария');
                    }
                })
                .catch(() => alert('Ошибка при сохранении комментария'));
            });
        });
    });
});

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
