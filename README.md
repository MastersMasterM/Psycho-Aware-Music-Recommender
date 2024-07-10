# Psycho-Aware Rule-Based Music Recommendation System

This project is a psycho-aware rule-based music recommendation system. It integrates personality traits, emotional states, and various music attributes to recommend music that aligns with the user's psychological profile. The system uses a Django web application, a forward-chaining inference engine based on rules, and a case-based engine that works on and updates historical data. The recommendation rules are designed to update over time based on user interaction and historical data.

## Knowledge Tree
![Knowledge Tree](https://github.com/MastersMasterM/Psycho-Aware-Music-Recommender/blob/master/Knowledge%20Tree.png)

## Features

- **Personality Traits and Emotional States Integration**: The system uses personality traits (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) and emotional states (Happy, Sad, Anxious, Calm) to tailor music recommendations.
- **Inference Engine**: Based on `rules.json`, the system infers suitable musical attributes (`Key Signatures`, `Tempo`, `Valence`, `Instrumentalness`) for users.
- **Case-Based Engine**: Retrieves the most similar items based on historical data and recommends additional music. Saves user attributes along with YouTube recommendations for future use.
- **Distance Metrics**: Uses Jaccard distance for key signatures and Hamming distance for categorical attributes (`Tempo`, `Valence`, `Instrumentalness`) to compute the distance between cases.
- **YouTube API Integration**: Retrieves music items directly from YouTube based on the recommendation rules.
- **Interactive Web Interface**: Developed using Django, the web app provides an intuitive interface for users to interact with the recommendation system.

## Prerequisites

- Google Developer Account (YouTube Data API v3 key)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/MastersMasterM/Psycho-Aware-Music-Recommender.git
    cd Psycho-Aware-Music-Recommender
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run initial setup**:
    ```bash
    cd recommender
    python manage.py migrate
    python populate_questions.py
    ```
5. **Setting Your API Key**:
- Open `recommender\inferenceengine\views.py` With a Text Editor
- Add Your API Key To `fetch_youtube_recommendations` Function
## Usage

1. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

2. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:8000/`.

3. **Interacting with the System**:
    - Answer the questionnaire to set up your personality traits and emotional state.
    - Receive music recommendations based on your responses and the dynamic rules in place.

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature-name
    ```
3. **Make your changes**.
4. **Commit your changes**:
    ```bash
    git commit -m 'Add some feature'
    ```
5. **Push to the branch**:
    ```bash
    git push origin feature-name
    ```
6. **Create a new Pull Request**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The development of this system was based on integrating psychological theories and musical attributes for a personalized music experience.
