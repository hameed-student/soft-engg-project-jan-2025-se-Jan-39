
@celery.task(name="extract_video_transcripts")
def extract_video_transcripts(content_id):
    with app.app_context():
        content = db.session.get(CourseContent, content_id)
        if not content:
            return {"error": "Course content not found"}

        # Extract video ID from YouTube URL
        youtube_patterns = [
            r'(?:v=|/)([a-zA-Z0-9_-]{11})',  # For standard and shared URLs
            r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',  # For shortened youtu.be URLs
            r'(?:embed/)([a-zA-Z0-9_-]{11})'  # For embed URLs
        ]

        video_id = None
        for pattern in youtube_patterns:
            match = re.search(pattern, content.video_link)
            if match:
                video_id = match.group(1)
                break

        if not video_id:
            return {"error": "Invalid YouTube URL"}

        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([t["text"] for t in transcript_data])
        except Exception as e:
            return {"error": f"Transcript extraction failed: {str(e)}"}

        existing_transcript = CourseTranscript.query.filter_by(content_id=content.id).first()
        if existing_transcript:
            existing_transcript.transcript_text = transcript_text
        else:
            new_transcript = CourseTranscript(
                course_id=content.course_id, 
                content_id=content.id, 
                transcript_text=transcript_text
            )
            db.session.add(new_transcript)
        
        db.session.commit()
        generate_and_store_embeddings(content_id, transcript_text)
        return {"message": "Transcript extracted and stored successfully"} 