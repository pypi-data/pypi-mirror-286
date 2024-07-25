# Autovid
Python package to automate and simplify video creation.

## What It Does
Autovid simplifies the text-to-speech video creation process by producing beautifully edited videos with minimal commands. :sparkles:

https://github.com/user-attachments/assets/ff08d7fc-5804-4ec7-930b-4a55bc38a834

## :rocket: Getting Started

### Prerequisites
- Obtain a client key and secret from Reddit by creating an app [here](https://old.reddit.com/prefs/apps/).
- Install autovid via pip
   
   ```sh
   pip install autovid
   ```

### Usage
- Import autovid and update the Reddit API id and secret to let autovid access Reddit.
  ```py
   import autovid as av
   
   av.api_keys.client_id = "my_client_id"
   av.api_keys.client_secret = "my_client_secret"
   ```

- Autovid creates 'clips' that are combined to create the final video. Use the ```redditpostclip``` or ```redditcommentclip``` methods to create clips that can be passed to the ```makevideo``` method to generate the video.
   ```py
   q = [
      av.redditpostclip("https://www.reddit.com/r/reddit.com/comments/87/the_downing_street_memo/"),
      av.redditcommentclip("https://www.reddit.com/r/reddit.com/comments/87/comment/c16lbx4"),
   ]
   
   av.makevideo(queue=q)
   ```

That's it! You can find your final video saved as ```temp/final.mp4```!

### Advanced
You can pass in parameters to the ```makevideo``` method to tweak the final video.
- Adding background audio and video:
  
   ```py
   q = [
      av.redditpostclip("https://www.reddit.com/r/reddit.com/comments/87/the_downing_street_memo/"),
   ]
   
   av.makevideo(queue=q, background_audio_path="lofi_music.mp3", background_video_path="minecraft.mp4")
   ```
   Autovid will use these to add background music and videos to the final output. A 720p video works best!
