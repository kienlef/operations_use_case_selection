/**
 * Supply Chain Analytics - Presentation Navigation
 * Data2Value Initiative
 */

class Presentation {
  constructor(options = {}) {
    this.currentSlide = 0;
    this.slides = document.querySelectorAll('.slide');
    this.totalSlides = this.slides.length;
    
    this.options = {
      showProgress: true,
      showCounter: true,
      showNavButtons: true,
      enableKeyboard: true,
      enableSwipe: true,
      ...options
    };
    
    this.init();
  }
  
  init() {
    if (this.totalSlides === 0) return;
    
    this.createUI();
    this.bindEvents();
    this.goToSlide(0);
    this.updateURL();
  }
  
  createUI() {
    // Progress bar
    if (this.options.showProgress) {
      const progress = document.createElement('div');
      progress.className = 'progress-bar';
      progress.id = 'progress';
      document.body.appendChild(progress);
    }
    
    // Slide counter
    if (this.options.showCounter) {
      const counter = document.createElement('div');
      counter.className = 'slide-counter';
      counter.id = 'counter';
      document.body.appendChild(counter);
    }
    
    // Navigation buttons
    if (this.options.showNavButtons) {
      const nav = document.createElement('div');
      nav.className = 'nav-controls';
      nav.innerHTML = `
        <button class="nav-btn" id="prevBtn">← Previous</button>
        <button class="nav-btn" id="nextBtn">Next →</button>
      `;
      document.body.appendChild(nav);
    }
  }
  
  bindEvents() {
    // Keyboard navigation
    if (this.options.enableKeyboard) {
      document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ') {
          e.preventDefault();
          this.next();
        } else if (e.key === 'ArrowLeft') {
          e.preventDefault();
          this.prev();
        } else if (e.key === 'Home') {
          e.preventDefault();
          this.goToSlide(0);
        } else if (e.key === 'End') {
          e.preventDefault();
          this.goToSlide(this.totalSlides - 1);
        }
      });
    }
    
    // Button navigation
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (prevBtn) prevBtn.addEventListener('click', () => this.prev());
    if (nextBtn) nextBtn.addEventListener('click', () => this.next());
    
    // URL hash navigation
    window.addEventListener('hashchange', () => {
      const hash = window.location.hash.slice(1);
      const slideNum = parseInt(hash) - 1;
      if (!isNaN(slideNum) && slideNum >= 0 && slideNum < this.totalSlides) {
        this.goToSlide(slideNum);
      }
    });
    
    // Check initial hash
    const initialHash = window.location.hash.slice(1);
    const initialSlide = parseInt(initialHash) - 1;
    if (!isNaN(initialSlide) && initialSlide >= 0 && initialSlide < this.totalSlides) {
      this.goToSlide(initialSlide);
    }
    
    // Touch/swipe navigation
    if (this.options.enableSwipe) {
      let touchStartX = 0;
      let touchEndX = 0;
      
      document.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
      });
      
      document.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > 50) {
          if (diff > 0) this.next();
          else this.prev();
        }
      });
    }
  }
  
  goToSlide(index) {
    if (index < 0 || index >= this.totalSlides) return;
    
    // Remove active from current
    this.slides[this.currentSlide].classList.remove('active');
    
    // Set new current
    this.currentSlide = index;
    this.slides[this.currentSlide].classList.add('active');
    
    this.updateUI();
    this.updateURL();
  }
  
  next() {
    if (this.currentSlide < this.totalSlides - 1) {
      this.goToSlide(this.currentSlide + 1);
    }
  }
  
  prev() {
    if (this.currentSlide > 0) {
      this.goToSlide(this.currentSlide - 1);
    }
  }
  
  updateUI() {
    // Update progress
    const progress = document.getElementById('progress');
    if (progress) {
      const percentage = ((this.currentSlide + 1) / this.totalSlides) * 100;
      progress.style.width = `${percentage}%`;
    }
    
    // Update counter
    const counter = document.getElementById('counter');
    if (counter) {
      counter.textContent = `${this.currentSlide + 1} / ${this.totalSlides}`;
    }
    
    // Update buttons
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (prevBtn) prevBtn.disabled = this.currentSlide === 0;
    if (nextBtn) nextBtn.disabled = this.currentSlide === this.totalSlides - 1;
  }
  
  updateURL() {
    history.replaceState(null, '', `#${this.currentSlide + 1}`);
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.presentation = new Presentation();
});
