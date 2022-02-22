import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import pathlib

# COMP264 - Cloud Machine Learning
# Nestor Romero - 301133331

class SpeechService:
    '''
    This class encapsulates the functionality required to transform a give text into audio (speech)
    '''

    def __init__(self):
        self.client = boto3.client('polly')

        # output to website directory
        self.output_dir = pathlib.Path(__file__).resolve().parents[2] / 'Website'
        self.output_dir.resolve()

    def create_speech_from_text(self, input_text, audio_output_filename):
        try:

            # ssml - speech sysntesis markup language
            # ssml input to slow down voice speech and make it more understandable
            print(f'\n>>> Creating speech audio for : {input_text}\n')
            input_ssml = f'<speak><prosody rate="x-slow">{input_text}</prosody></speak>'

            # Request speech synthesis
            response = self.client.synthesize_speech(
                Text=input_ssml,
                OutputFormat="mp3",
                VoiceId="Kendra",
                TextType='ssml'
            )
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

        # Access response["AudioStream"]
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:

                # print(self.output_dir)
                
                output = os.path.join(
                    self.output_dir, f'{audio_output_filename}.mp3')
                
                try:
                    # Save audio to local file
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    print(error)
                    sys.exit(-1)

        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)


# service = SpeechService()
# # ssml - speech syntesis markup language
# service.create_speech_from_text('COMP264 is very good', 'audio_result')
