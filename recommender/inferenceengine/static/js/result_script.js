// result_script.js

document.addEventListener('DOMContentLoaded', function() {
    // YouTube API Key
    const apiKey = 'AIzaSyAj2QLlcj_8e6q_GXBSMthLGOTd_xMhGjg'; // Replace with your YouTube API Key
    const mood = '{{ user.user_mood }}';

    async function fetchYouTubeRecommendations() {
        try {
            // Fetch recommendations from YouTube Data API
            const response = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&q=${mood} music&type=video&key=${apiKey}&maxResults=5`);
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const data = await response.json();
            const recommendations = data.items;
            const recommendationsContainer = document.getElementById('youtubeRecommendations');

            // Clear any existing content
            recommendationsContainer.innerHTML = '';

            // Check if recommendations are available
            if (recommendations.length > 0) {
                recommendations.forEach(video => {
                    const videoElement = document.createElement('div');
                    videoElement.className = 'youtube-video';
                    videoElement.innerHTML = `
                        <img src="${video.snippet.thumbnails.medium.url}" alt="${video.snippet.title}">
                        <a href="https://www.youtube.com/watch?v=${video.id.videoId}" target="_blank">${video.snippet.title}</a>
                    `;
                    recommendationsContainer.appendChild(videoElement);
                });
            } else {
                recommendationsContainer.innerHTML = '<p>No recommendations available.</p>';
            }
        } catch (error) {
            console.error('Error fetching YouTube recommendations:', error);
            document.getElementById('youtubeRecommendations').innerHTML = '<p>Error fetching recommendations.</p>';
        }
    }

    fetchYouTubeRecommendations();
});
