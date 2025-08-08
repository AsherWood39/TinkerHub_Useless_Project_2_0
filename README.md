# Intrusive Thoughts Generator 🎨✨

Turn ordinary images into extraordinary stories! This project uses computer vision and AI to find interesting patterns in images and weave creative tales about what it discovers.

## 🌟 Features

- **Pattern Detection**: Sophisticated image processing to highlight interesting shapes and patterns
- **Creative Storytelling**: AI-powered narrative generation that creates engaging stories based on detected patterns
- **Interactive Interface**: User-friendly Streamlit interface for easy image uploads and story generation
- **Artistic Interpretation**: Combines computer vision with creative AI to see the extraordinary in the ordinary

## 🛠️ Technologies Used

- **Streamlit**: For the interactive web interface
- **OpenCV**: For image processing and pattern detection
- **Groq AI**: For creative story generation
- **Python PIL**: For image handling and manipulation

## 🚀 Getting Started

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Create a `.env` file
   - Add your Groq API key: `GROQ_API_KEY=your_key_here`

4. Run the application:
   ```bash
   streamlit run main.py
   ```

## 📝 How It Works

1. **Upload**: Choose any image you'd like to analyze
2. **Process**: The app detects interesting patterns and creates a high-contrast outline
3. **Generate**: AI examines the patterns and creates a creative story about what it sees
4. **Enjoy**: Read the whimsical interpretation of your image!

## 🎯 Project Structure

- `main.py`: The main Streamlit application
- `image_cleaning.py`: Image processing and pattern detection
- `groq_interpretation.py`: AI story generation using Groq
- `requirements.txt`: Required Python packages

## 🎨 Example

Upload a crumpled paper, coffee stain, or any image with interesting patterns, and watch as the AI:
1. Detects and highlights intriguing shapes
2. Creates a story based on what it "sees"
3. Engages in a playful conversation about the details it noticed

## 🔑 Environment Variables

Required environment variables:
- `GROQ_API_KEY`: Your Groq AI API key

## 📚 Contributing

Feel free to:
- Open issues
- Submit pull requests
- Suggest new features
- Share your creative results!

## 🌈 Future Enhancements

- Image generation based on stories
- Multiple interpretation styles
- Pattern recognition improvements
- User story collections

## 📄 License

This project is open source and available under the MIT License.

---

Created with ❤️ for the joy of finding magic in the mundane!
Just a useless project
