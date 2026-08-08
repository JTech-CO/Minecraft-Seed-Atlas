(() => {
  'use strict';

  const seeds = Array.isArray(window.MINECRAFT_SEEDS) ? window.MINECRAFT_SEEDS : [];

  const CATEGORY_RULES = [
    { id: 'village', label: '마을', keywords: ['마을', '정착지', '산촌', '거점'] },
    { id: 'island', label: '섬', keywords: ['섬', '군도', '해양 마을'] },
    { id: 'cave', label: '동굴·지하', keywords: ['동굴', '지하', '폐광', '딥다크', '고대 도시', '트라이얼 챔버', '협곡', '공동'] },
    { id: 'mountain', label: '산악', keywords: ['산악', '산맥', '설산', '고산', '고봉', '분화구', '칼데라', '절벽', '싱크홀', '고지대', 'Y 2'] },
    { id: 'structure', label: '구조물', keywords: ['삼림 대저택', '대저택', '사원', '피라미드', '요새', '엔드 포탈', '전초기지', '폐허 포탈', '이글루', '해저 신전', '구조 중첩'] },
    { id: 'cherry', label: '벚나무숲', keywords: ['벚나무숲', '벚꽃'] },
    { id: 'sulfur', label: '유황', keywords: ['유황', '간헐천'] },
    { id: 'ocean', label: '해양', keywords: ['바다', '해양', '해안', '난파선', '호수', '수면', '빙산'] },
    { id: 'desert', label: '사막', keywords: ['사막', '배드랜드', '메사', '테라코타', '건조'] },
    { id: 'snow', label: '빙설', keywords: ['설원', '눈 덮인', '얼어붙은', '빙설', '얼음', '타이가'] },
    { id: 'jungle', label: '정글', keywords: ['정글', '맹그로브', '대나무'] },
    { id: 'survival', label: '생존', keywords: ['생존', '하드코어', '자원 제한', '클래식', '장기 생존', '초반 생존', '표류자', '캐스트어웨이'] }
  ];

  const state = {
    query: '',
    version: 'all',
    category: 'all',
    sort: 'curated'
  };

  const elements = {
    form: document.querySelector('#filter-form'),
    search: document.querySelector('#seed-search'),
    searchClear: document.querySelector('#search-clear'),
    versionFilter: document.querySelector('#version-filter'),
    category: document.querySelector('#category-filter'),
    sort: document.querySelector('#sort-order'),
    random: document.querySelector('#random-seed'),
    reset: document.querySelector('#reset-filters'),
    emptyReset: document.querySelector('#empty-reset'),
    grid: document.querySelector('#seed-grid'),
    empty: document.querySelector('#empty-state'),
    summary: document.querySelector('#result-summary'),
    toast: document.querySelector('#copy-toast')
  };

  let currentResults = [];
  let toastTimer = null;
  const customSelectControllers = new Map();

  function closeCustomSelects(exceptSelect = null) {
    customSelectControllers.forEach((controller, select) => {
      if (select !== exceptSelect) controller.close();
    });
  }

  function createCustomSelect(select) {
    if (!select || customSelectControllers.has(select)) return;

    const control = select.closest('.select-field__control');
    if (!control) return;

    const field = select.closest('.select-field');
    const label = field?.querySelector(`label[for="${select.id}"]`);
    const originalArrow = control.querySelector(':scope > svg');

    control.classList.add('has-custom-select');
    select.classList.add('select-field__native');
    select.tabIndex = -1;
    select.setAttribute('aria-hidden', 'true');
    if (originalArrow) originalArrow.hidden = true;

    if (label && !label.id) label.id = `${select.id}-label`;

    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'custom-select__trigger';
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');

    const valueText = document.createElement('span');
    valueText.className = 'custom-select__value';
    valueText.id = `${select.id}-value`;

    const arrow = document.createElement('span');
    arrow.className = 'custom-select__arrow';
    arrow.setAttribute('aria-hidden', 'true');
    arrow.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18"><path d="m7 9 5 5 5-5H7Z"/></svg>';

    trigger.append(valueText, arrow);
    if (label) trigger.setAttribute('aria-labelledby', `${label.id} ${valueText.id}`);
    else trigger.setAttribute('aria-label', select.getAttribute('aria-label') || select.name || '선택');

    const menu = document.createElement('div');
    menu.className = 'custom-select__menu';
    menu.id = `${select.id}-listbox`;
    menu.setAttribute('role', 'listbox');
    menu.setAttribute('aria-labelledby', label?.id || valueText.id);
    menu.hidden = true;
    trigger.setAttribute('aria-controls', menu.id);

    const optionButtons = Array.from(select.options).map((option, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'custom-select__option';
      button.dataset.value = option.value;
      button.dataset.optionIndex = String(index);
      button.setAttribute('role', 'option');
      button.setAttribute('aria-selected', String(option.selected));
      button.textContent = option.textContent;
      menu.append(button);
      return button;
    });

    control.append(trigger, menu);

    function update() {
      const selectedIndex = Math.max(0, select.selectedIndex);
      const selected = select.options[selectedIndex];
      valueText.textContent = selected?.textContent || '';
      optionButtons.forEach((button, index) => {
        const isSelected = index === selectedIndex;
        button.setAttribute('aria-selected', String(isSelected));
        button.tabIndex = isSelected ? 0 : -1;
      });
    }

    function focusOption(index) {
      const normalizedIndex = Math.min(Math.max(index, 0), optionButtons.length - 1);
      optionButtons[normalizedIndex]?.focus();
    }

    function open(focusIndex = Math.max(0, select.selectedIndex)) {
      closeCustomSelects(select);
      menu.hidden = false;
      control.classList.add('is-open');
      trigger.setAttribute('aria-expanded', 'true');
      window.requestAnimationFrame(() => focusOption(focusIndex));
    }

    function close({ restoreFocus = false } = {}) {
      if (menu.hidden) return;
      menu.hidden = true;
      control.classList.remove('is-open');
      trigger.setAttribute('aria-expanded', 'false');
      if (restoreFocus) trigger.focus();
    }

    function choose(value) {
      if (select.value === value) {
        update();
        close({ restoreFocus: true });
        return;
      }
      select.value = value;
      select.dispatchEvent(new Event('change', { bubbles: true }));
      update();
      close({ restoreFocus: true });
    }

    trigger.addEventListener('click', () => {
      if (menu.hidden) open();
      else close();
    });

    trigger.addEventListener('keydown', (event) => {
      if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
        event.preventDefault();
        const current = Math.max(0, select.selectedIndex);
        if (event.key === 'ArrowDown') open(current + 1);
        if (event.key === 'ArrowUp') open(current - 1);
        if (event.key === 'Home') open(0);
        if (event.key === 'End') open(optionButtons.length - 1);
      }
      if (event.key === 'Escape') close();
    });

    menu.addEventListener('click', (event) => {
      const option = event.target.closest('.custom-select__option');
      if (option) choose(option.dataset.value);
    });

    menu.addEventListener('keydown', (event) => {
      const active = document.activeElement?.closest('.custom-select__option');
      const index = active ? Number(active.dataset.optionIndex) : Math.max(0, select.selectedIndex);

      if (event.key === 'ArrowDown') {
        event.preventDefault();
        focusOption(index + 1);
      } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        focusOption(index - 1);
      } else if (event.key === 'Home') {
        event.preventDefault();
        focusOption(0);
      } else if (event.key === 'End') {
        event.preventDefault();
        focusOption(optionButtons.length - 1);
      } else if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        if (active) choose(active.dataset.value);
      } else if (event.key === 'Escape') {
        event.preventDefault();
        close({ restoreFocus: true });
      } else if (event.key === 'Tab') {
        close();
      }
    });

    select.addEventListener('change', update);
    customSelectControllers.set(select, { update, close, open });
    update();
  }

  function initCustomSelects() {
    [elements.category, elements.sort].forEach(createCustomSelect);

    document.addEventListener('pointerdown', (event) => {
      if (!event.target.closest('.has-custom-select')) closeCustomSelects();
    });

    document.addEventListener('focusin', (event) => {
      customSelectControllers.forEach((controller, select) => {
        const control = select.closest('.has-custom-select');
        if (control && !control.contains(event.target)) controller.close();
      });
    });

    window.addEventListener('resize', () => closeCustomSelects());
  }

  function syncCustomSelect(select) {
    customSelectControllers.get(select)?.update();
  }

  function normalize(value) {
    return String(value ?? '').trim().toLocaleLowerCase('ko-KR');
  }

  function getTags(description) {
    const normalized = normalize(description);
    const matched = CATEGORY_RULES.filter((rule) => rule.keywords.some((keyword) => normalized.includes(normalize(keyword))));
    return matched.length ? matched : [{ id: 'other', label: '특이 지형', keywords: [] }];
  }

  const enrichedSeeds = seeds.map((seed, index) => ({
    ...seed,
    sourceIndex: index,
    tags: getTags(seed.description)
  }));

  function readUrlState() {
    const params = new URLSearchParams(window.location.search);
    const query = params.get('q') || '';
    const version = params.get('version') || 'all';
    const category = params.get('category') || 'all';
    const sort = params.get('sort') || 'curated';

    state.query = query;
    state.version = ['all', '26.2', '26.1', '1.21'].includes(version) ? version : 'all';
    state.category = ['all', ...CATEGORY_RULES.map((rule) => rule.id)].includes(category) ? category : 'all';
    state.sort = ['curated', 'description', 'seed-asc', 'seed-desc'].includes(sort) ? sort : 'curated';

    elements.search.value = state.query;
    elements.category.value = state.category;
    elements.sort.value = state.sort;
    syncCustomSelect(elements.category);
    syncCustomSelect(elements.sort);
    updateVersionButtons();
    updateSearchClear();
  }

  function syncUrl() {
    const params = new URLSearchParams();
    if (state.query) params.set('q', state.query);
    if (state.version !== 'all') params.set('version', state.version);
    if (state.category !== 'all') params.set('category', state.category);
    if (state.sort !== 'curated') params.set('sort', state.sort);

    const queryString = params.toString();
    const nextUrl = `${window.location.pathname}${queryString ? `?${queryString}` : ''}${window.location.hash}`;

    // Local file previews can restrict History API writes. GitHub Pages uses HTTPS,
    // where URL state works normally. A blocked write must never interrupt rendering.
    try {
      window.history.replaceState(null, '', nextUrl);
    } catch (error) {
      // No-op for restricted file:// contexts.
    }
  }

  function updateVersionButtons() {
    elements.versionFilter.querySelectorAll('[data-version]').forEach((button) => {
      const isActive = button.dataset.version === state.version;
      button.setAttribute('aria-pressed', String(isActive));
    });
  }

  function updateSearchClear() {
    elements.searchClear.hidden = elements.search.value.length === 0;
  }

  function compareBigInt(a, b) {
    const left = BigInt(a.seed);
    const right = BigInt(b.seed);
    if (left === right) return 0;
    return left < right ? -1 : 1;
  }

  function getFilteredSeeds() {
    const query = normalize(state.query);
    const queryParts = query.split(/\s+/).filter(Boolean);

    const filtered = enrichedSeeds.filter((seed) => {
      if (state.version !== 'all' && seed.version !== state.version) return false;
      if (state.category !== 'all' && !seed.tags.some((tag) => tag.id === state.category)) return false;

      if (queryParts.length) {
        const haystack = normalize([
          seed.version,
          seed.seed,
          seed.description,
          ...seed.tags.map((tag) => tag.label)
        ].join(' '));
        if (!queryParts.every((part) => haystack.includes(part))) return false;
      }

      return true;
    });

    if (state.sort === 'description') {
      return filtered.sort((a, b) => a.description.localeCompare(b.description, 'ko-KR'));
    }
    if (state.sort === 'seed-asc') {
      return filtered.sort(compareBigInt);
    }
    if (state.sort === 'seed-desc') {
      return filtered.sort((a, b) => compareBigInt(b, a));
    }
    return filtered.sort((a, b) => a.sourceIndex - b.sourceIndex);
  }

  function appendHighlightedText(container, text, query) {
    const normalizedQuery = normalize(query);
    if (!normalizedQuery || normalizedQuery.includes(' ') || /^-?\d+$/.test(normalizedQuery)) {
      container.textContent = text;
      return;
    }

    const source = String(text);
    const normalizedSource = normalize(source);
    const index = normalizedSource.indexOf(normalizedQuery);
    if (index < 0) {
      container.textContent = source;
      return;
    }

    container.append(document.createTextNode(source.slice(0, index)));
    const mark = document.createElement('mark');
    mark.textContent = source.slice(index, index + normalizedQuery.length);
    container.append(mark, document.createTextNode(source.slice(index + normalizedQuery.length)));
  }

  function copyIconSvg() {
    return '<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path d="M8 2h11a2 2 0 0 1 2 2v11h-2V4H8V2ZM5 6h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2Zm0 2v12h10V8H5Z"/></svg>';
  }

  function checkIconSvg() {
    return '<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path d="m9.2 16.2-4.4-4.4L3.4 13.2 9.2 19 21 7.2l-1.4-1.4-10.4 10.4Z"/></svg>';
  }

  function createSeedCard(seed, visibleIndex) {
    const article = document.createElement('article');
    article.className = 'seed-card';
    article.dataset.version = seed.version;
    article.id = `seed-card-${seed.sourceIndex + 1}`;

    const body = document.createElement('div');
    body.className = 'seed-card__body';

    const meta = document.createElement('div');
    meta.className = 'seed-card__meta';

    const version = document.createElement('span');
    version.className = 'version-badge';
    version.textContent = `JAVA ${seed.version}`;

    const number = document.createElement('span');
    number.className = 'card-number';
    number.textContent = `#${String(seed.sourceIndex + 1).padStart(3, '0')}`;
    number.title = `문서 수록 번호 ${seed.sourceIndex + 1} · 현재 결과 ${visibleIndex + 1}번째`;

    meta.append(version, number);

    const description = document.createElement('p');
    description.className = 'seed-card__description';
    appendHighlightedText(description, seed.description, state.query);

    const tags = document.createElement('div');
    tags.className = 'seed-card__tags';
    seed.tags.slice(0, 4).forEach((tag) => {
      const badge = document.createElement('span');
      badge.className = 'terrain-tag';
      badge.textContent = tag.label;
      tags.append(badge);
    });

    body.append(meta, description, tags);

    const copyButton = document.createElement('button');
    copyButton.className = 'seed-copy';
    copyButton.type = 'button';
    copyButton.dataset.seed = seed.seed;
    copyButton.setAttribute('aria-label', `시드 ${seed.seed} 클립보드에 복사`);

    const code = document.createElement('code');
    code.textContent = seed.seed;

    const icon = document.createElement('span');
    icon.className = 'seed-copy__icon';
    icon.innerHTML = copyIconSvg();

    copyButton.append(code, icon);
    article.append(body, copyButton);
    return article;
  }

  function updateSummary(count) {
    const total = enrichedSeeds.length;
    const filters = [];
    if (state.version !== 'all') filters.push(`Java ${state.version}`);
    if (state.category !== 'all') {
      const category = CATEGORY_RULES.find((rule) => rule.id === state.category);
      if (category) filters.push(category.label);
    }
    if (state.query) filters.push(`“${state.query}”`);

    elements.summary.replaceChildren();
    const strong = document.createElement('strong');
    strong.textContent = String(count);
    elements.summary.append(strong, document.createTextNode(` / ${total}개의 시드를 표시합니다${filters.length ? ` · ${filters.join(' · ')}` : ''}.`));
  }

  function render() {
    currentResults = getFilteredSeeds();
    const fragment = document.createDocumentFragment();
    currentResults.forEach((seed, index) => fragment.append(createSeedCard(seed, index)));

    elements.grid.replaceChildren(fragment);
    elements.grid.hidden = currentResults.length === 0;
    elements.grid.setAttribute('aria-busy', 'false');
    elements.empty.hidden = currentResults.length !== 0;
    updateSummary(currentResults.length);
    syncUrl();
  }

  async function writeClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    textarea.style.pointerEvents = 'none';
    document.body.append(textarea);
    textarea.select();
    const copied = document.execCommand('copy');
    textarea.remove();
    if (!copied) throw new Error('Clipboard copy failed');
  }

  function showToast(seed) {
    window.clearTimeout(toastTimer);
    const message = elements.toast.querySelector('span');
    message.textContent = `${seed} 복사 완료`;
    elements.toast.hidden = false;
    toastTimer = window.setTimeout(() => {
      elements.toast.hidden = true;
    }, 1800);
  }

  async function handleCopy(button) {
    const seed = button.dataset.seed;
    try {
      await writeClipboard(seed);
      button.classList.add('is-copied');
      const icon = button.querySelector('.seed-copy__icon');
      icon.innerHTML = checkIconSvg();
      button.setAttribute('aria-label', `시드 ${seed} 복사 완료`);
      showToast(seed);
      window.setTimeout(() => {
        button.classList.remove('is-copied');
        icon.innerHTML = copyIconSvg();
        button.setAttribute('aria-label', `시드 ${seed} 클립보드에 복사`);
      }, 1500);
    } catch (error) {
      window.prompt('자동 복사가 제한되었습니다. 아래 시드를 직접 복사하세요.', seed);
    }
  }

  function resetFilters({ focusSearch = false } = {}) {
    state.query = '';
    state.version = 'all';
    state.category = 'all';
    state.sort = 'curated';
    elements.search.value = '';
    elements.category.value = 'all';
    elements.sort.value = 'curated';
    syncCustomSelect(elements.category);
    syncCustomSelect(elements.sort);
    updateVersionButtons();
    updateSearchClear();
    render();
    if (focusSearch) elements.search.focus();
  }

  function chooseRandomSeed() {
    if (!currentResults.length) return;
    const selected = currentResults[Math.floor(Math.random() * currentResults.length)];
    const card = document.querySelector(`#seed-card-${selected.sourceIndex + 1}`);
    if (!card) return;
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.classList.remove('is-highlighted');
    window.requestAnimationFrame(() => card.classList.add('is-highlighted'));
    window.setTimeout(() => card.classList.remove('is-highlighted'), 1400);
  }

  function updateStats() {
    const counts = enrichedSeeds.reduce((acc, seed) => {
      acc.all += 1;
      acc[seed.version] = (acc[seed.version] || 0) + 1;
      return acc;
    }, { all: 0 });

    document.querySelectorAll('[data-stat]').forEach((node) => {
      node.textContent = String(counts[node.dataset.stat] || 0);
    });

    elements.versionFilter.querySelectorAll('[data-version]').forEach((button) => {
      const count = button.querySelector('span');
      if (count) count.textContent = String(counts[button.dataset.version] || 0);
    });
  }

  elements.form.addEventListener('submit', (event) => {
    event.preventDefault();
  });

  elements.search.addEventListener('input', () => {
    state.query = elements.search.value.trim();
    updateSearchClear();
    render();
  });

  elements.searchClear.addEventListener('click', () => {
    state.query = '';
    elements.search.value = '';
    updateSearchClear();
    render();
    elements.search.focus();
  });

  elements.versionFilter.addEventListener('click', (event) => {
    const button = event.target.closest('[data-version]');
    if (!button) return;
    state.version = button.dataset.version;
    updateVersionButtons();
    render();
  });

  elements.category.addEventListener('change', () => {
    state.category = elements.category.value;
    render();
  });

  elements.sort.addEventListener('change', () => {
    state.sort = elements.sort.value;
    render();
  });

  elements.grid.addEventListener('click', (event) => {
    const button = event.target.closest('.seed-copy');
    if (button) handleCopy(button);
  });

  elements.random.addEventListener('click', chooseRandomSeed);
  elements.reset.addEventListener('click', (event) => {
    event.preventDefault();
    resetFilters();
  });
  elements.emptyReset.addEventListener('click', () => resetFilters({ focusSearch: true }));

  window.addEventListener('popstate', () => {
    readUrlState();
    render();
  });

  initCustomSelects();
  updateStats();
  readUrlState();
  render();
})();
