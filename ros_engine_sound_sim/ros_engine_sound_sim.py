import threading
import time
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

from ros_engine_sound_sim import engine_factory
from ros_engine_sound_sim.audio_device import AudioDevice

class RosEngineSoundSim(Node):
    def __init__(self, name="ros_engine_sound_sim"):
        super().__init__(name)

        self._sub = None
        self._engines = []
        self._streams = []
        
        self._max_throttle_vel = 0.5
        self._max_engine_rpm = 1.0
        
        self._set_engine_rpm = 0

    
    def configure(self):
        self._engines = [
            engine_factory.lero1(),
            engine_factory.lero2(),
            engine_factory.lero3()
        ]
        
        self._audio_device = AudioDevice()

        self._sub = self.create_subscription(TwistStamped, "/cmd_vel", self.cmd_vel_cb, 10)
        
        self._sound_thread = threading.Thread(target=self.sound_thread_loop, args=())
        self._sound_thread.start()
        
        for engine in self._engines:
            self._streams.append(self._audio_device.play_stream(engine.gen_audio))

        
    def destroy_node(self):
        self._sound_thread.join()
        for stream in self._streams:
            stream.close()
        self._audio_device.close()

        return super().destroy_node()

    def cmd_vel_cb(self, msg: TwistStamped):
        total_vel = math.sqrt(msg.twist.linear.x * msg.twist.linear.x + msg.twist.linear.y * msg.twist.linear.y + msg.twist.linear.z * msg.twist.linear.z)
        self._set_engine_rpm = total_vel / self._max_throttle_vel * self._max_engine_rpm
        
    def sound_thread_loop(self):
        while rclpy.ok():
            for engine in self._engines:
                #engine.set_rpm(self._set_engine_rpm)
                engine.throttle(self._set_engine_rpm)
            time.sleep(0.02)
