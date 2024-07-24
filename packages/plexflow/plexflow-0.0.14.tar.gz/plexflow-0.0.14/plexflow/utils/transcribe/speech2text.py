import whisper

def transcribe_audio(file_path, model: str = 'medium'):
    """
    Transcribes an audio file using the Whisper model.

    Args:
        file_path (str): The path to the audio file to transcribe.

    Returns:
        str: The transcription of the audio file.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        Exception: If there is an error loading the model or transcribing the audio.

    Example:
        >>> transcribe_audio('path/to/your/audio/file.mp3')
        'This is the transcribed text from your audio file.'

    Note:
        This function assumes that you have the Whisper model available locally.
    """
    try:
        # Check if the file exists
        with open(file_path, 'rb') as f:
            pass
    except FileNotFoundError as e:
        raise e

    try:
        # Load the Whisper model
        model = whisper.load_model(model)

        # Transcribe the audio
        result = model.transcribe(file_path)

        return result["text"]
    except Exception as e:
        raise e
