const query = document.querySelector.bind(document);
const removeComma = string => string.slice(0, string.length - 1).trim()

const isInvalid = stringInput => {
    const inputs = Array.from(query('.pois').children).map(input => input.firstElementChild.textContent);
    return  !/^[A-Za-z0-9]{3,}/.test(stringInput) ||
        inputs.some(name => name === removeComma(stringInput)) ||
        query('.pois').children.length >= 10;
}

function modifyTags(e) {
    if(e.key === ',') {
        if(isInvalid(e.target.value)) {
            e.target.value = '';
            return;
        }
        addTag(e.target.value);
        e.target.value = '';
    }
    // if(e.key === 'Backspace' && !e.target.value.length) {
    //     deleteTag(null, query('.pois').children.length - 1);
    // }
}

function addTag(textValue) {
    const tag = document.createElement('div'),
    tagName = document.createElement('label'),
    remove = document.createElement('span');

    tagName.setAttribute('class', 'tag-name');
    tagName.textContent = removeComma(textValue);

    remove.setAttribute('class', 'remove');
    remove.textContent = 'X';
    remove.addEventListener('click', deleteTag);

    tag.setAttribute('class', 'poi');
    tag.appendChild(tagName);
    tag.appendChild(remove);

    query('.pois').appendChild(tag);
}

function deleteTag(e, i = Array.from(query('.pois').children).indexOf(e.target.parentElement)) {
    const index = query('.pois').getElementsByClassName('poi')[i];
    query('.pois').removeChild(index);
}

function focus() {
    query('#id_poi').focus();
}

query('.poi-inputs').addEventListener('click', focus);
query('#id_poi').addEventListener('keyup', modifyTags);