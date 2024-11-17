// Clean and efficient preloader handling
document.addEventListener('DOMContentLoaded', () => {
    const mainContent = document.querySelector('main');
    const preloader = document.getElementById('preloader');

    // Force initial states
    mainContent.style.display = 'block';
    mainContent.style.opacity = '0';
    preloader.style.opacity = '1';

    // Trigger transition
    window.setTimeout(() => {
        preloader.style.opacity = '0';
        mainContent.style.opacity = '1';
        
        window.setTimeout(() => {
            preloader.style.display = 'none';
            startCounters();
        }, 1000);
    }, 1500);
});

function startCounters() {
    const counters = document.querySelectorAll('.number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000;
        const frames = 60;
        const increment = target / frames;
        let current = 0;
        
        const animate = () => {
            current += increment;
            if(current < target) {
                counter.innerHTML = Math.floor(current).toLocaleString();
                window.requestAnimationFrame(animate);
            } else {
                counter.innerHTML = target.toLocaleString();
            }
        };
        
        counter.innerHTML = '0';
        window.requestAnimationFrame(animate);
    });
}
    const starsContainer = document.createElement('div');
    starsContainer.className = 'stars';
    document.body.appendChild(starsContainer);
      for (let i = 0; i < 50; i++) {
          const star = document.createElement('div');
          star.className = 'star';
          star.style.left = `${Math.random() * 100}%`;
          star.style.top = `${Math.random() * 100}%`;
          star.style.setProperty('--duration', `${1 + Math.random() * 2}s`); // Faster blinking (1-3s range)
          starsContainer.appendChild(star);
      }
// Add this to your existing script
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

function createWindEffect() {
    const container = document.createElement('div');
    container.className = 'particles-container';
    document.body.appendChild(container);

    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.width = `${2 + Math.random() * 3}px`;
        particle.style.height = particle.style.width;
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.setProperty('--duration', `${8 + Math.random() * 15}s`);
        container.appendChild(particle);
    }
}

createWindEffect();
