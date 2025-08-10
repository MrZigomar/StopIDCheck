/*
 * JavaScript for the StopVerifAge static site.
 * Handles data loading, search, filtering and page navigation.
 */

// Fetch JSON data once and cache it. Returns a Promise resolving to the array of sites.
let sitesCache = null;
async function loadSites() {
  // Use embedded data from window.sitesData.  This avoids fetch restrictions
  // when the site is served from the filesystem.  If sitesCache is already
  // populated, return it immediately.
  if (sitesCache) {
    return sitesCache;
  }
  if (window.sitesData && Array.isArray(window.sitesData.sites)) {
    sitesCache = window.sitesData.sites;
    return sitesCache;
  }
  // Fallback: try to fetch if running on a web server
  try {
    const response = await fetch('data/sites.json');
    const data = await response.json();
    sitesCache = data.sites;
    return sitesCache;
  } catch (error) {
    console.error('Impossible de charger les données des sites :', error);
    sitesCache = [];
    return sitesCache;
  }
}

// Utility: get query parameter from current URL
function getQueryParam(param) {
  const params = new URLSearchParams(window.location.search);
  return params.get(param) || '';
}

// Populate index page with categories and recent sites
async function initIndexPage() {
  const sites = await loadSites();
  // compute unique categories
  const categoriesSet = new Set();
  sites.forEach(site => {
    site.category.forEach(cat => categoriesSet.add(cat));
  });
  const categories = Array.from(categoriesSet).sort();
  // insert categories into DOM
  const categoriesContainer = document.getElementById('categories');
  categories.forEach(cat => {
    const card = document.createElement('div');
    card.className = 'site-card';
    card.innerHTML = `
      <h3>${cat}</h3>
      <p>Voir les sites de cette catégorie.</p>
    `;
    card.addEventListener('click', () => {
      window.location.href = `list.html?category=${encodeURIComponent(cat)}`;
    });
    categoriesContainer.appendChild(card);
  });
  // show recent sites (last 4 by id)
  const recent = sites
    .slice()
    .sort((a, b) => b.id - a.id)
    .slice(0, 4);
  const recentContainer = document.getElementById('recent-sites');
  recent.forEach(site => {
    const card = document.createElement('div');
    card.className = 'site-card';
    card.innerHTML = `
      <h4>${site.name}</h4>
      <p><strong>Catégorie :</strong> ${site.category.join(', ')}</p>
      <p><strong>Méthode :</strong> ${site.verification_type}</p>
    `;
    card.addEventListener('click', () => {
      window.location.href = `site.html?id=${site.id}`;
    });
    recentContainer.appendChild(card);
  });
  // handle search form submission
  const searchForm = document.getElementById('search-form');
  if (searchForm) {
    searchForm.addEventListener('submit', event => {
      event.preventDefault();
      const query = document.getElementById('search-input').value.trim();
      if (query) {
        window.location.href = `list.html?q=${encodeURIComponent(query)}`;
      } else {
        window.location.href = 'list.html';
      }
    });
  }
}

// Populate list page with filter results
async function initListPage() {
  const sites = await loadSites();
  const q = getQueryParam('q').toLowerCase();
  const category = getQueryParam('category');
  const country = getQueryParam('country');
  // compute available categories and countries for filters
  const categoriesSet = new Set();
  const countriesSet = new Set();
  sites.forEach(site => {
    site.category.forEach(cat => categoriesSet.add(cat));
    site.country.forEach(c => countriesSet.add(c));
  });
  const categories = Array.from(categoriesSet).sort();
  const countries = Array.from(countriesSet).sort();
  // fill filter dropdowns
  const catSelect = document.getElementById('filter-category');
  categories.forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat;
    opt.textContent = cat;
    if (cat === category) opt.selected = true;
    catSelect.appendChild(opt);
  });
  const countrySelect = document.getElementById('filter-country');
  countries.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c;
    opt.textContent = c;
    if (c === country) opt.selected = true;
    countrySelect.appendChild(opt);
  });
  // handle filter form submission
  const filterForm = document.getElementById('filter-form');
  filterForm.addEventListener('submit', event => {
    event.preventDefault();
    const qVal = document.getElementById('filter-search').value.trim();
    const catVal = catSelect.value;
    const countryVal = countrySelect.value;
    const params = new URLSearchParams();
    if (qVal) params.set('q', qVal);
    if (catVal) params.set('category', catVal);
    if (countryVal) params.set('country', countryVal);
    window.location.search = params.toString();
  });
  // filter sites according to query
  let filtered = sites;
  if (q) {
    filtered = filtered.filter(site => site.name.toLowerCase().includes(q));
  }
  if (category) {
    filtered = filtered.filter(site => site.category.includes(category));
  }
  if (country) {
    filtered = filtered.filter(site => site.country.includes(country));
  }
  // sort by name
  filtered.sort((a, b) => a.name.localeCompare(b.name));
  // render table
  const tableBody = document.getElementById('sites-table-body');
  tableBody.innerHTML = '';
  filtered.forEach(site => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><a href="site.html?id=${site.id}">${site.name}</a></td>
      <td>${site.category.join(', ')}</td>
      <td>${site.verification_type}</td>
      <td>${site.status}</td>
    `;
    tableBody.appendChild(row);
  });
  if (filtered.length === 0) {
    const emptyRow = document.createElement('tr');
    emptyRow.innerHTML = `<td colspan="4">Aucun site ne correspond à vos critères.</td>`;
    tableBody.appendChild(emptyRow);
  }
  // prefill search input
  document.getElementById('filter-search').value = q;
}

// Populate site detail page
async function initSitePage() {
  const sites = await loadSites();
  const id = parseInt(getQueryParam('id'), 10);
  const site = sites.find(s => s.id === id);
  if (!site) {
    document.getElementById('site-container').innerHTML = '<p>Site introuvable.</p>';
    return;
  }
  // insert site details
  document.getElementById('site-name').textContent = site.name;
  const urlEl = document.getElementById('site-url');
  urlEl.href = site.url;
  urlEl.textContent = site.url;
  document.getElementById('site-category').textContent = site.category.join(', ');
  document.getElementById('site-description').textContent = site.description;
  document.getElementById('site-verif').textContent = site.verification_type;
  document.getElementById('site-context').textContent = site.context;
  document.getElementById('site-date').textContent = site.date_in_effect;
  document.getElementById('site-status').textContent = site.status;
  document.getElementById('site-country').textContent = site.country.join(', ');
  document.getElementById('site-sources').textContent = site.sources.join(', ');
  // alternatives
  const altContainer = document.getElementById('alternatives');
  altContainer.innerHTML = '';
  if (site.alternatives && site.alternatives.length > 0) {
    site.alternatives.forEach(alt => {
      const div = document.createElement('div');
      div.className = 'alt-card';
      div.innerHTML = `
        <h4>${alt.name}</h4>
        <p><a href="${alt.url}" target="_blank" rel="noopener">${alt.url}</a></p>
        <p>${alt.description}</p>
      `;
      altContainer.appendChild(div);
    });
  } else {
    altContainer.textContent = 'Aucune alternative connue.';
  }
}

// Suggest page feedback (no backend storage)
function initSuggestPage() {
  const form = document.getElementById('suggest-form');
  form.addEventListener('submit', event => {
    event.preventDefault();
    alert('Merci pour votre suggestion ! Nous la prendrons en compte après vérification.');
    form.reset();
  });
}

// Determine which page initializer to run based on body data attribute
document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const page = body.dataset.page;
  if (page === 'index') {
    initIndexPage();
  } else if (page === 'list') {
    initListPage();
  } else if (page === 'site') {
    initSitePage();
  } else if (page === 'suggest') {
    initSuggestPage();
  }
});