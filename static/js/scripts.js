document.addEventListener("DOMContentLoaded", () => {
    const phoneText = document.getElementById("phone-text");
    const container = document.getElementById("phone-container");
    const tooltip = document.getElementById("copied-tooltip");
    const myNumber = "+380123456789";

    if (phoneText) {
        container.addEventListener("click", () => {
            // Показать номер рядом с текстом
            phoneText.textContent = myNumber;

            // Подпрыгивание
            container.classList.remove("jump");
            void container.offsetWidth; // перезапуск анимации
            container.classList.add("jump");

            // Tooltip над контейнером
            tooltip.style.display = "block";
            const rect = container.getBoundingClientRect();
            tooltip.style.top = rect.top - 25 + window.scrollY + "px"; 
            tooltip.style.left = rect.left + rect.width/2 + window.scrollX + "px";

            // Скрыть через 1.5 сек
            setTimeout(() => {
                tooltip.style.display = "none";
            }, 1500);

            // Копировать номер
            navigator.clipboard.writeText(myNumber).catch(err => console.log(err));
        });
    }
});
