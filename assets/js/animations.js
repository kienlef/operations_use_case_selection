/**
 * Supply Chain Analytics - Animation Utilities
 * Data2Value Initiative
 */

// Intersection Observer for scroll animations
const observeElements = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fadeIn');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  
  document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
  });
};

// Stagger animation for lists
const staggerList = (selector, delay = 100) => {
  const items = document.querySelectorAll(selector);
  items.forEach((item, index) => {
    item.style.animationDelay = `${index * delay}ms`;
    item.classList.add('animate-fadeIn');
  });
};

// Counter animation
const animateCounter = (element, target, duration = 2000) => {
  let start = 0;
  const increment = target / (duration / 16);
  
  const updateCounter = () => {
    start += increment;
    if (start < target) {
      element.textContent = Math.floor(start);
      requestAnimationFrame(updateCounter);
    } else {
      element.textContent = target;
    }
  };
  
  updateCounter();
};

// Typing animation
const typeWriter = (element, text, speed = 50) => {
  let i = 0;
  element.textContent = '';
  
  const type = () => {
    if (i < text.length) {
      element.textContent += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  };
  
  type();
};

// Slide-specific animations
const animateSlideElements = (slide) => {
  const animatedElements = slide.querySelectorAll('[data-animate]');
  animatedElements.forEach((el, index) => {
    const animationType = el.dataset.animate || 'fadeIn';
    const delay = el.dataset.delay || index * 100;
    
    setTimeout(() => {
      el.classList.add(`animate-${animationType}`);
    }, delay);
  });
};

// Export for use
window.SCAAnimations = {
  observeElements,
  staggerList,
  animateCounter,
  typeWriter,
  animateSlideElements
};

document.addEventListener('DOMContentLoaded', observeElements);
