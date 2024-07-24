'''
This module contains the main functionality of the autovid package
'''

import os
import moviepy.editor as mp

from autovid.utils import reddit_handler
from autovid.utils.clip import Clip

__all__ = ['redditpostclip','redditcommentclip','makevideo']

def redditpostclip(url):
    ''' 
    Fetches reddit post from url and converts it to an autovid Clip
    '''
    
    submission = reddit_handler._fetch_post(url)
    audio_str = submission.title + submission.selftext
    clip = Clip(audio_str)
    clip._selenium_wrapper = {'type':'post','url':'https://www.reddit.com/'+submission.id}
    return clip

def redditcommentclip(url):
    ''' 
    Fetches reddit comment from url and converts it to an autovid Clip
    '''

    submission = reddit_handler._fetch_comment(url)
    audio_str = submission.body
    clip = Clip(audio_str)
    clip._selenium_wrapper = {'type':'comment','url':'https://www.reddit.com'+submission.permalink}
    return clip

def textclip(text):
    ''' 
    Converts basic text into autovid Clip
    '''

    return Clip(text)

def makevideo(queue:list, background_video_path="", background_audio_path=""):
    '''
    Generates final rendered video from autovid Clips
    '''

    path = 'temp/'
    if not os.path.exists(path):
        os.makedirs(path)

    videoclips = []
    num = 1
    for clip in queue:
        image_path = path + f'img_{num}.png'
        audio_path = path + f'audio_{num}.mp3'

        clip._gen_audio(audio_path)
        clip._gen_img(image_path)
        
        audioclip = mp.AudioFileClip(audio_path)
        videoclip = (mp.ImageClip(image_path)
                .set_duration(audioclip.duration)
                .set_pos(("center","center"))
            )

        videoclip = videoclip.set_audio(audioclip)
        videoclip = videoclip.set_opacity(0.95)

        videoclips.append(videoclip)
    
        num += 1
    
    videoclip = mp.concatenate_videoclips(videoclips)

    if not background_video_path:
        background = mp.ColorClip(size=(1280,720), color=[0,0,0], duration=videoclip.duration)
    else:
        background = mp.VideoFileClip(background_video_path)
        background = background.subclip(0,videoclip.duration)

    videoclip = videoclip.set_pos(("center","center"))

    videoclip = mp.CompositeVideoClip([background, videoclip])

    if background_audio_path:
        background_audio = mp.AudioFileClip(background_audio_path)
        background_audio =  background_audio.volumex(0.25)
        background_audio = background_audio.set_duration(videoclip.duration)

        videoclip = videoclip.set_audio(mp.CompositeAudioClip([videoclip.audio, background_audio]))

    videoclip.write_videofile('temp/final.mp4', fps=24)