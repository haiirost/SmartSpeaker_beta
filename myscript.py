#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
subprocess.call('export GOOGLE_APPLICATION_CREDENTIALS=/home/stas/SS/google.json', shell=True)
subprocess.call('export GCLOUD_PROJECT=smartspeaker-207611', shell=True)



def run_quickstart():
    # [START speech_quickstart]
    import io
    import os
    import re

    volume = 20
    # Imports the Google Cloud client library
    # [START migration_import]
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    # [END migration_import]
    subprocess.call('amixer set \'Master\' mute', shell=True)
    print('Volume Mute')
    print('Start rec to file')
    subprocess.call('rec -r 16k -e signed-integer -b 16 -c 1 resources/audio.raw trim 0 5', shell=True)
    print('Stop rec to file')
    subprocess.call('amixer set \'Master\' ' + str(volume) + ' unmute', shell=True)
    print('Volume unmute')
    # Instantiates a client
    # [START migration_client]
    client = speech.SpeechClient()
    # [END migration_client]

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'audio.raw')

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print(result.alternatives[0].transcript)
	
	if re.search(r'\bradio\b', result.alternatives[0].transcript):
	    if re.search(r'\bstart\b', result.alternatives[0].transcript):
		#subprocess.call('', shell=True)
		subprocess.call('amixer set \'Master\' ' + volume + ' unmute', shell=True)
		subprocess.call('mplayer -slave -quiet '+'http://online-radioroks2.tavrmedia.ua/RadioROKS_NewRock'+' </dev/null >/dev/null 2>&1 &', shell=True)
	        print("Radio On")
            if re.search(r'\bstop\b', result.alternatives[0].transcript):
		subprocess.call('pkill mplayer', shell=True)
	        print("Radio Off")

	if re.search(r'\bvolume\b', result.alternatives[0].transcript):
	    if re.search(r'\boff\b', result.alternatives[0].transcript):
		subprocess.call('amixer set \'Master\' mute', shell=True)
		print("volume off")
	    if re.search(r'\bmute\b', result.alternatives[0].transcript):
		subprocess.call('amixer set \'Master\' mute', shell=True)
		print("volume mute")
	    if re.search(r'\bon\b', result.alternatives[0].transcript):
		subprocess.call('amixer set \'Master\' ' + volume + ' unmute', shell=True)
		print("volume on")
	    if re.search(r'\b20\b', result.alternatives[0].transcript):
		volume = 20
		subprocess.call('amixer set \'Master\' 20% unmute', shell=True)
		print("volume 20%")
    	    if re.search(r'\b50\b', result.alternatives[0].transcript):
		volume = 50
		subprocess.call('amixer set \'Master\' 50% unmute', shell=True)
		print("volume 50%")
    
    # [END speech_quickstart]


if __name__ == '__main__':
    if True:
        run_quickstart()

    print("Script end")
