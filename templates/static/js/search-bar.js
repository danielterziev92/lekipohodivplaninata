const searchQuery = document.getElementById('search-query');
searchQuery.addEventListener('input', getHikesFromSearchQuery);
const searchResultElement = document.getElementById('search-result');

async function getHikesFromSearchQuery(e) {
    e.preventDefault();
    const queryElement = e.currentTarget
    const query = encodeURIComponent(e.currentTarget.value);


    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const url = `${window.location.origin}/api/hikes/search/?q=${query}`;

    const response = await fetch(url);

    if (!response.ok) {
        const result = await response.json();
        throw new Error(result.message);
    }

    const data = await response.json();

    const dataElements = [];

    const isDataEmpty = data.hike.length === 0
    if (isDataEmpty) {
        if (searchResultElement.classList.contains('show')) {
            searchResultElement.classList.remove('show');
        }
    } else {
        if (!searchResultElement.classList.contains('show')) {
            searchResultElement.classList.add('show')
        }

        for (const id in data.hike) {
            const {_id, title, slug, duration, event_date, main_picture, type, price, pk} = data.hike[id];

            dataElements.push(
                createElement('li', '', '', '', [
                    createElement('figure', '', {}, '', [
                        createElement('img', '', {src: `https://res.cloudinary.com/dujto2hys/${main_picture}`})
                    ]),
                    createElement('a', title, {href: `${window.location.origin}/hike/${pk}/${slug}`}),
                    createElement('div', '', {className: 'info'}, '', [
                        createElement('p', '', {className: 'event-date'}, '', [
                            createElement('i', '', {className: 'fa-regular fa-calendar-days'}),
                            createElement('span', event_date),
                        ]),
                        createElement('p', '', {className: 'type'}, '', [
                            createElement('i', '', {className: 'fa-solid fa-mountain-sun'}),
                            createElement('span', type),
                        ]),
                        createElement('p', '', {className: 'duration'}, '', [
                            createElement('i', '', {className: 'fa-solid fa-clock'}),
                            createElement('span', duration),
                        ]),
                        createElement('p', '', {className: 'price'}, '', [
                            createElement('i', '', {className: 'fa-regular fa-money-bill-1'}),
                            createElement('span', `${price} лв.`)
                        ]),
                        new Date(event_date) > new Date()
                            ? createElement('button', 'Запиши ме', '', changeLocation)
                            : createElement('button', 'Запиши ме', {disabled: true})
                    ])
                ])
            );
        }

        searchResultElement.replaceChildren(...dataElements)

    }
}


function changeLocation(e) {
    e.preventDefault();

    const absoluteUrl = e.currentTarget.parentElement.parentElement.querySelector('a').href

    const url = new URL(absoluteUrl);
    const relativeUrl = url.pathname;

    window.location.pathname = relativeUrl
}

function createElement(type, text, attributes, callback, children) {
    const element = document.createElement(type);

    if (text) {
        element.textContent = text
    }

    if (attributes) {
        for (const prop in attributes) {
            element[prop] = attributes[prop];
        }
    }

    if (callback) {
        element.addEventListener('click', callback);
    }

    if (children) {
        for (const child of children) {
            element.appendChild(child);
        }
    }

    return element;
}