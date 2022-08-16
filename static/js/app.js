class TypeWriter {
  constructor(spanElement, sentences, wait = 1500) {
    this.spanElement = spanElement;
    this.sentences = sentences;
    this.txt = "";
    this.sentenceIndex = 0;
    this.wait = parseInt(wait, 10);
    this.isDeleting = false;
    this.type()
  }

  type() {
    const currentIndex = this.sentenceIndex % this.sentences.length;
    const fullSentence = `${this.sentences[currentIndex]} `;
    
    if (this.isDeleting) {
      this.txt = fullSentence.substring(0, this.txt.length - 1)
    } else {
      this.txt = fullSentence.substring(0, this.txt.length + 1)
    }
    this.spanElement.innerHTML = `<span class="txt"> ${this.txt}</span>`;

    let typeSpeed = 60;
    if (this.isDeleting) {
      typeSpeed /= 2;
    }

    if (!this.isDeleting && this.txt === fullSentence) {
      typeSpeed = this.wait
      this.isDeleting = true;
    } else if (this.isDeleting && this.txt === '') {
      this.isDeleting = false;
      this.sentenceIndex++;
      typeSpeed = 300;
    }
    setTimeout(() => this.type(), typeSpeed);
  }
}
  
function typewriterInit() {
  const spanElement = document.querySelector('.index-typewriter');
  const sentences = ["Upload Your Resume", "Review Your Details", "Apply Within Seconds"];
  new TypeWriter(spanElement, sentences, wait = 1500);
}

function showFileName(event) {
  const textbox = document.querySelector('.file-name-textbox');
  let fileInfoArea = document.querySelectorAll('.uploaded-file-name')
  const input = event.srcElement;
  const fileName = input.files[0].name;

  if (fileInfoArea.length == 0) {
      fileInfoArea = document.createElement('div');
      fileInfoArea.classList.add('uploaded-file-name');
      fileInfoArea.textContent = 'File name: ' + fileName;
      textbox.appendChild(fileInfoArea);
  } else {
      fileInfoArea = fileInfoArea[0];
  }
  fileInfoArea.textContent = 'File name: ' + fileName;
}

function createPosting(posting) {
  const postingTemplate = document.querySelector('#posting-template').content;
  const templateCopy = document.importNode(postingTemplate, true);
  templateCopy.querySelector('.posting-title').textContent = posting['title'];
  templateCopy.querySelector('.company').textContent = posting['company'];
  templateCopy.querySelector('.location').textContent = posting['location'];
  templateCopy.querySelector('.confidence-header').textContent = `${Math.ceil(posting.confidence * 1000)/10}%`;
  templateCopy.querySelector('.description').textContent = posting['description'];
  templateCopy.querySelector('.external-link').href = posting['link'];
  templateCopy.querySelector('.select-label').for = `${posting['link']}`;
  selectBox = templateCopy.querySelector('#checkbox');
  selectBox.id = `${posting['link']}`
  document.querySelector('.jobs-section').appendChild(templateCopy);
}

function waitForChange() {
  allPostings = document.querySelectorAll('.select-checkbox');
  for (posting of allPostings) {
    posting.addEventListener('change', sendCheckboxState);
  }
}