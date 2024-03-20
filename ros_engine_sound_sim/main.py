from ros_engine_sound_sim import controls
from ros_engine_sound_sim import engine_factory
from ros_engine_sound_sim.audio_device import AudioDevice
import random
import threading
import time

# engine = engine_factory.v_four_90_deg()
# engine = engine_factory.w_16()
# engine = engine_factory.v_8_LS()
# engine = engine_factory.inline_5_crossplane()
# engine = engine_factory.inline_6()
# engine = engine_factory.boxer_4_crossplane_custom([1, 1, 0, 0])  # (rando := random.randrange(360)))
# engine = engine_factory.inline_4_1_spark_plug_disconnected()
# engine = engine_factory.inline_4()
# engine = engine_factory.boxer_4_half()
# engine = engine_factory.random()
#engine = engine_factory.fake_rotary_2rotor()
#engine = engine_factory.V_12()

audio_device1 = AudioDevice()

def play_audio(audio_device1, engine1, start_delay):
    time.sleep(start_delay)
    stream1 = audio_device1.play_stream(engine1.gen_audio)
    
    print('\nEngine is running...')
    # print(rando)
    
    try:
        controls.capture_input(engine1)  # blocks until user exits
    except KeyboardInterrupt:
        pass
    
    print('Exiting...')
    stream1.close()

engine1 = engine_factory.lero1()
engine2 = engine_factory.lero2()
engine3 = engine_factory.lero3()
t1 = threading.Thread(target=play_audio, args=(audio_device1, engine1, 0.0))
t2 = threading.Thread(target=play_audio, args=(audio_device1, engine2, 0.08))
t3 = threading.Thread(target=play_audio, args=(audio_device1, engine3, 0.06))
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()
audio_device1.close()
