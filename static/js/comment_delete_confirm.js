document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-comment-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const commentDiv = btn.closest('.comment');

            // Скрываем кнопку ×
            btn.style.display = 'none';

            // Создаем блок подтверждения
            const confirmDiv = document.createElement('div');
            confirmDiv.style.display = 'flex';
            confirmDiv.style.gap = '5px';
            confirmDiv.style.marginTop = '5px';

            const text = document.createElement('span');
            text.textContent = 'Точно хотите удалить?';

            const yesBtn = document.createElement('button');
            yesBtn.textContent = 'Да';
            yesBtn.style.backgroundColor = '#f03e3e';
            yesBtn.style.color = 'white';
            yesBtn.style.border = 'none';
            yesBtn.style.borderRadius = '5px';
            yesBtn.style.padding = '2px 5px';
            yesBtn.style.cursor = 'pointer';

            const noBtn = document.createElement('button');
            noBtn.textContent = 'Отмена';
            noBtn.style.backgroundColor = '#ccc';
            noBtn.style.color = 'black';
            noBtn.style.border = 'none';
            noBtn.style.borderRadius = '5px';
            noBtn.style.padding = '2px 5px';
            noBtn.style.cursor = 'pointer';

            confirmDiv.appendChild(text);
            confirmDiv.appendChild(yesBtn);
            confirmDiv.appendChild(noBtn);

            commentDiv.querySelector('.comment-actions').appendChild(confirmDiv);

            // Обработчик отмены
            noBtn.addEventListener('click', () => {
                confirmDiv.remove();
                btn.style.display = 'inline-block';
            });

            // Обработчик подтверждения через fetch POST
            yesBtn.addEventListener('click', () => {
                const url = btn.getAttribute('data-url');

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (response.ok) {
                        // Просто убираем комментарий с экрана
                        commentDiv.remove();
                    } else {
                        alert('Ошибка при удалении комментария');
                    }
                })
                .catch(() => alert('Ошибка при удалении комментария'));
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
