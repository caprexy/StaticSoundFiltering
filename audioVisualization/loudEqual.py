from pydub import AudioSegment

def match_target_amplitude(sound,target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

sound = AudioSegment.from_file("test.wav","wav")
normalized_sound = match_target_amplitude(sound,-20)
normalized_sound.export("test2.wav",format ="wav")
print 'a'
