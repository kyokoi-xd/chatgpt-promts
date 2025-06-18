// script.js

// фикс стили навбара при скролле
window.addEventListener('scroll', () => {
  document.querySelector('.navbar')
          .classList.toggle('scrolled', window.scrollY > 20);
});

let totalPrompts = 0;
let visibleCount = 0;
let filterQuery = '';
let promptCopiedText = 'Copied!';
let currentLang = 'en';

// инициализация: count — общее число карточек, lang — 'ru' или 'en', copiedText — текст тултипа
function initPrompts(count, lang, copiedText) {
  totalPrompts = count;
  visibleCount = 12;
  filterQuery = '';
  promptCopiedText = copiedText;
  currentLang = lang;

  // обработчики
  document.getElementById('searchInput')
          .addEventListener('keyup', filterPrompts);
  document.getElementById('showMoreBtn')
          .addEventListener('click', () => {
    visibleCount += 12;
    updateDisplay();
  });
  document.getElementById('currentYear').innerText =
    new Date().getFullYear();

  // задержка анимации карточек
  document.querySelectorAll('.prompt-card')
          .forEach((card, i) => {
    card.style.animationDelay = `${i * 50}ms`;
  });

  // сразу показ
  updateDisplay();
}

// копирование в буфер
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    const tooltip = document.createElement('div');
    tooltip.innerText = promptCopiedText;
    tooltip.className = 'copy-tooltip';
    document.body.append(tooltip);
    setTimeout(() => tooltip.remove(), 1200);
  });
}

// разворачивание текста
function toggleFullText(button) {
  const textDiv = button
    .closest('.prompt-text-container')
    .querySelector('.prompt-text');

  // берем язык из атрибута кнопки, а не из textDiv
  const isRu = button.getAttribute('data-lang') === 'ru';

  // переключаем класс
  const expanded = textDiv.classList.toggle('expanded');

  // обновляем текст кнопки
  if (expanded) {
    button.innerText = isRu ? 'Свернуть ↑' : 'Show less ↑';
  } else {
    button.innerText = isRu ? 'Читать полностью ↓' : 'Read more ↓';
  }
}

function scrollToRandomPrompt() {
  // 1) Получаем список всех data-index
  const allIndices = Array.from(document.querySelectorAll('.prompt-card'))
                          .map(card => card.dataset.index);
  if (!allIndices.length) return;

  // 2) Выбираем случайный индекс
  const randIdx = allIndices[
    Math.floor(Math.random() * allIndices.length)
  ];

  // 3) Находим карточку с этим data-index
  const target = document.querySelector(`.prompt-card[data-index="${randIdx}"]`);
  if (!target) return;

  // 4) Делаем её видимой (чтобы не скроллить к скрытому элементу)
  target.style.display = '';
  const container = document.getElementById('promptsList');
  container.appendChild(target); // перемещаем в конец списка

  // 5) Скроллим и подсвечиваем
  target.scrollIntoView({ behavior: 'smooth', block: 'center' });

  target.classList.add('highlight-flash');
  setTimeout(() => target.classList.remove('highlight-flash'), 1200);
}

// обновление списка карточек
function updateDisplay() {
  const q = filterQuery.toLowerCase();
  const cards = Array.from(document.querySelectorAll('.prompt-card'));
  let shown = 0;

  cards.forEach(card => {
    const ruAct  = (card.dataset.ruAct   || '').toLowerCase();
    const ruTxt  = (card.dataset.ruPrompt|| '').toLowerCase();
    const enAct  = (card.dataset.enAct   || '').toLowerCase();
    const enTxt  = (card.dataset.enPrompt|| '').toLowerCase();
    const match = ruAct.includes(q)
               || ruTxt.includes(q)
               || enAct.includes(q)
               || enTxt.includes(q);

    if (match && shown < visibleCount) {
      card.style.display = '';
      highlightMatch(card, q);
      shown++;
    } else {
      card.style.display = 'none';
    }
  });

  // показать/скрыть кнопку «ещё»
  const btn = document.getElementById('showMoreBtn');
  if (btn) {
    btn.style.display = (shown < totalPrompts && shown >= visibleCount)
                      ? '' : 'none';
  }
}

// подсветка вхождений
function highlightMatch(card, query) {
  const txtEL = card.querySelector('.prompt-text');
  const raw = (currentLang === 'ru')
            ? card.dataset.ruPrompt
            : card.dataset.enPrompt;
  if (query) {
    const re = new RegExp(`(${query.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')})`, 'gi');
    txtEL.innerHTML = raw.replace(re, '<mark>$1</mark>');
  } else {
    txtEL.innerHTML = raw;
  }
}

// поиск
function filterPrompts(e) {
  filterQuery = e.target.value.trim();
  visibleCount = 12;
  updateDisplay();
}

// глобально доступны
window.initPrompts           = initPrompts;
window.copyToClipboard       = copyToClipboard;
window.toggleFullText        = toggleFullText;
window.scrollToRandomPrompt  = scrollToRandomPrompt;
