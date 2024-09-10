const path = '.'

async function fetchMapping() {
  const mapping = await fetch(path + '/mapping.json')
  const mappingJson = await mapping.json()
  return mappingJson
}

function embedElements(mapping, parent, path) {
  let children = mapping.children
  children.sort((a, b) => {
    if (a.type === 'folder' && b.type !== 'folder') {
      return -1
    } else if (a.type !== 'folder' && b.type === 'folder') {
      return 1
    } else {
      return 0
    }
  })

  let images = [];
  let files = [];

  children.map(child => {
    if (child.type === 'folder') {
      parent.innerHTML += `<details><summary>${child.name}</summary><div class="flex flex-col gap-2 px-5 py-2" id="${child.name}"></div></details>`;
      embedElements(child, document.getElementById(child.name), path + '/' + child.name);
    } else {
      switch (child.type) {
        case 'image':
          images.push(child.name)
          break
        case 'file':
          files.push(child.name)
          break
      }
    }
  })

  let imagesContainer = document.createElement('div')
  imagesContainer.className = 'w-full flex flex-row flex-wrap gap-5'
  let filesContainer = document.createElement('ul')
  filesContainer.className = 'w-full list-disc'

  images.map(image => {
    imagesContainer.innerHTML += `<a href="${path}/${image}" target="_blank" class="p-1 border-2 border-blue-500 rounded-md"><img src="${path}/${image}" id="${image}" alt="${image}" class="max-h-48 w-auto "/></a>`
  })

  files.map(file => {
    filesContainer.innerHTML += `<li><a href="${path}/${file}" target="_blank" class="text-blue-500 underline">${file}</a></li>`
  })
  
  if (images.length > 0)
    parent.appendChild(imagesContainer)
  if (files.length > 0)
    parent.appendChild(filesContainer)
}

var mapping = {}

fetchMapping().then(data => {
  mapping = data
  embedElements(mapping, document.getElementById('root'), path);
  console.log(mapping)
})


