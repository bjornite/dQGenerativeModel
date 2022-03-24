import random
import time

class dQGenerativeModel():
    def __init__(self) -> None:
        self.S = ["s0", "s1"]
        self.C = 10
        self.r = 3
        self.kappa = 2
        self.dQ = {"s0": 1/self.C, "s1": self.r/self.C}
        self.P = {"s0": (["s1"], [1]), "s1": (["s0"], [1])}
        self.T = {("s0", "s1"): self.kappa/2, ("s1", "s0"): self.kappa/2}
        self.current_state = "s0"
        self.last_get_delay_time = time.time()
        self.time_remaining_in_current_state = 0
        self.next_state = "uninitiated"
    
    def get_delay(self, time_now):
        if self.next_state != "uninitiated":
            if time_now < self.last_get_delay_time + self.time_remaining_in_current_state:
                self.time_remaining_in_current_state = self.time_remaining_in_current_state - (time_now - self.last_get_delay_time)
                self.last_get_delay_time = time_now
                return self.dQ[self.current_state]
            else:
                self.current_state = self.next_state
                self.last_get_delay_time = self.last_get_delay_time + self.time_remaining_in_current_state
        delay = 0
        while(self.last_get_delay_time + delay <= time_now):
            self.last_get_delay_time = self.last_get_delay_time + delay
            possible_next_states, probabilities = self.P[self.current_state]
            self.next_state = random.choices(possible_next_states, weights=probabilities, k=1)[0]
            delay = self.T[(self.current_state, self.next_state)]
        self.time_remaining_in_current_state = self.last_get_delay_time + delay - time_now
        self.last_get_delay_time = time_now
        return self.dQ[self.current_state]
    