window.addEventListener("load", typewriterInit);

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
    setTimeout(() => this.type(), typeSpeed)
  }
}

function typewriterInit() {
  const spanElement = document.querySelector('.index-typewriter');
  const sentences = ["Upload Your Resume", "Review Your Details", "Apply Within Seconds"]
  new TypeWriter(spanElement, sentences, wait = 1500)
}