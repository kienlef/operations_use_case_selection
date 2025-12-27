/**
 * Supply Chain Analytics - Video Loader
 * Dynamically loads YouTube embeds based on manifest
 */

class VideoLoader {
  constructor(manifestPath = '/videos/video-manifest.json') {
    this.manifestPath = manifestPath;
    this.manifest = null;
    this.init();
  }
  
  async init() {
    try {
      const response = await fetch(this.manifestPath);
      this.manifest = await response.json();
      this.loadVideos();
    } catch (error) {
      console.log('Video manifest not found, using placeholders');
    }
  }
  
  loadVideos() {
    const containers = document.querySelectorAll('[data-video-id]');
    
    containers.forEach(container => {
      const videoKey = container.dataset.videoId;
      const videoConfig = this.manifest?.videos?.[videoKey];
      
      if (videoConfig?.id && videoConfig.status === 'published') {
        this.embedVideo(container, videoConfig.id);
      } else {
        this.showPlaceholder(container, videoConfig?.title || 'Video Coming Soon');
      }
    });
  }
  
  embedVideo(container, videoId) {
    const options = this.manifest?.embed_options || {};
    const params = new URLSearchParams(options).toString();
    
    container.innerHTML = `
      <iframe
        src="https://www.youtube.com/embed/${videoId}?${params}"
        title="YouTube video"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: var(--radius-lg, 8px);"
      ></iframe>
    `;
  }
  
  showPlaceholder(container, title) {
    container.innerHTML = `
      <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: var(--color-bg-alt, #f5f5f5); display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: var(--radius-lg, 8px); color: var(--color-text-muted, #666);">
        <i class="fab fa-youtube" style="font-size: 4rem; margin-bottom: 1rem; color: #ff0000;"></i>
        <p style="font-weight: 600;">${title}</p>
        <p style="font-size: 0.875rem;">Coming Soon</p>
        <a href="${this.manifest?.channel?.url || 'https://youtube.com/@data2value'}" 
           target="_blank" 
           style="margin-top: 1rem; padding: 0.5rem 1rem; background: var(--color-primary, #333); color: white; border-radius: 4px; text-decoration: none; font-size: 0.875rem;">
          Subscribe to Data2Value
        </a>
      </div>
    `;
  }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
  new VideoLoader();
});
