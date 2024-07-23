# mdlsum (Media Downloader & Summarizer)

**mdlsum** is a Python package designed to download, transcribe, and summarize media. Currently, it supports YouTube videos, with plans to expand to podcasts and other media formats. This tool aims to provide basic yet useful summaries, with future iterations planned to enhance its utility for personal and family use.

## Features
- **Download YouTube Videos**: Fetches the best audio quality available from YouTube videos.
- **Transcribe Audio**: Utilizes Whisper to convert audio into text, including timestamps.
- **Summarize Transcriptions**: Uses a language model to generate concise summaries formatted as a table of contents with timestamps.

## Installation
To install mdlsum-cli, run:

```sh
pip install mdlsum-cli
```

## Usage
#### Set Environment Variable:
Ensure that the `OPENAI_API_KEY` is set in your environment:
```sh
export OPENAI_API_KEY=your_openai_api_key_here
```

#### Running the Application
To use the application, simply provide a YouTube URL:
```sh
mdlsum "https://www.youtube.com/watch?v=example"
```

## Technical Details
### Overview
The `mdlsum` package combines several powerful tools to achieve its functionality:
1.	`yt-dlp`: A versatile downloader used to fetch YouTube videos.
2.	`ffmpeg`: Converts downloaded video audio into the desired format.
3.	whisper.cpp: A lightweight and efficient implementation of OpenAI’s Whisper model, used for transcribing audio.
4.	OpenAI’s GPT-3.5-turbo: Provides the summarization capabilities, transforming transcriptions into concise summaries.
5.	Typer: Facilitates the creation of the command-line interface (CLI).

### How it works

#### Downloading Videos
The process begins with the `download.py` module, where yt-dlp downloads the audio from a YouTube video. The downloaded audio is then converted to a 16-bit WAV file using ffmpeg. This step ensures that the audio is in a suitable format for transcription.

#### Transcribing Audio
Next, the `transcribe.py` module takes over. It uses whisper.cpp to transcribe the audio into text, ensuring that timestamps are included. This transcription process involves the following steps:

- Checking and downloading the Whisper model if not already present.
- Running the transcription using the Whisper model to generate a text file with timestamps.

#### Summarizing Transcriptions
The final step is handled by the `summarize.py` module. This module sends the transcribed text to OpenAI’s API to generate a summary. The API call includes instructions to format the summary as a table of contents with timestamps. This step ensures that the summary is easy to navigate and understand.

### Technologies Used
- yt-dlp: for downloading YouTube videos and other media
- ffmpeg: for audio conversion
- whisper.cpp: for transcription locally on your PC
- OpenAI API: for summarization
- Typer: for building the CLI

## Building the Project
### Development Process
The project was developed incrementally, starting with setting up the basic CLI structure using Typer. Each major feature (downloading, transcribing, summarizing) was implemented and tested separately before being integrated into the final application. The development process involved:

1.	Setting up a virtual environment for dependency management.
2.	Implementing and testing each feature in isolation.
3.	Integrating the features into a cohesive CLI tool.
4.	Packaging the project for distribution.

## Acknowledgements
This project wouldn't have been possible without the incredible work of the following individuals and organizations:

- OpenAI & Anthropic for the Whisper model and their language model APIs
- Georgi Gerganov for his incredible work on whisper.cpp `https://github.com/ggerganov/whisper.cpp`
- yt-dlp `https://github.com/yt-dlp/yt-dlp`
- Typer `https://github.com/tiangolo/typer` 

## License
See [LICENSE](https://github.com/nirvana47/mdlsum/blob/main/LICENSE).

## Future Plans
- Expand support to include podcasts and other media formats
- Improve summary quality and customization options
- Add advanced features like specifying models and timestamps
- Build a library of podcasts and YouTube video summaries that is searchable

---

*This project is a work in progress, and I look forward to iterating on it to make it even more useful. Thank you for checking it out!*

SidRT