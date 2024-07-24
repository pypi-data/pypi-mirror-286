import torch


class FourierGaitGenerator:
    # foot height type
    FOOT_HEIGHT_TYPE_LINEAR = 0
    FOOT_HEIGHT_TYPE_SMOOTH = 1

    # ratio change type
    RATIO_CHANGE_INCREASE_BASE = 1.003
    RATIO_CHANGE_DECREASE_BASE = 0.997

    # swing middle type
    SWING_MIDDLE_TYPE_LINEAR = 0
    SWING_MIDDLE_TYPE_ACCURATE = 1

    def __init__(self,
                 num_envs,
                 num_feet,
                 phase_offset=None,
                 dt: float = 0.02,
                 foot_height_target: float = 0.10,
                 device=None, ):
        self.num_envs = num_envs
        self.num_feet = num_feet
        if device is None:
            self.device = "cuda:0"
        else:
            self.device = device

        self.x = torch.ones(self.num_envs, self.num_feet, dtype=torch.float, device=self.device)
        self.y = torch.zeros(self.num_envs, self.num_feet, dtype=torch.float, device=self.device)

        # phase offset (different oscillators have different phase offset)
        self.phase_offset = torch.zeros(self.num_envs, self.num_feet, dtype=torch.float, device=self.device)
        self.set_phase_offset(phase_offset=phase_offset)

        self.dt = dt
        self.cycle_r = 1.0

        self.rate = 1.0
        self.frequency = 1.0

        self.foot_height = 0.0
        self.foot_height_target = foot_height_target

        self.ratio_contact = 0.5 * torch.ones(self.num_envs, self.num_feet, dtype=torch.float, device=self.device)
        self.b: float = 1000.0  # decide precision of the ratio_contact, the higher, the more precise

        # ratio change type
        # Note: related to dt !!! The smaller the dt, the smaller the ratio_change !!!
        self.ratio_change = torch.ones(self.num_envs, self.num_feet, dtype=torch.float, device=self.device)
        self.ratio_change_increase = self.RATIO_CHANGE_INCREASE_BASE ** (self.dt / 0.001)  # compared to increase_ratio in 0.001 second
        self.ratio_change_decrease = self.RATIO_CHANGE_DECREASE_BASE ** (self.dt / 0.001)  # compared to decrease_ratio in 0.001 second
        self.cycle_r_min = 0.001

    # ---------------------------------------------------------------
    def _gamma(self, y):
        term1 = torch.pi / ((1 - self.ratio_contact) * (torch.exp(-self.b * y) + 1))
        term2 = torch.pi / ((0 + self.ratio_contact) * (torch.exp(self.b * y) + 1))
        return term1 + term2

    def _cpg_hopf_oscillator(self):
        # Parameters for the Hopf oscillator
        r = torch.sqrt(self.x ** 2 + self.y ** 2)
        gamma = self._gamma(self.y)

        # alpha Controls the rate of convergence to the limit cycle
        alpha = self.frequency * (self.rate)
        # omega Natural frequency of the oscillator
        omega = self.frequency * gamma

        # Hopf oscillator differential equations
        dx = alpha * (self.cycle_r ** 2 - r ** 2) * self.x - omega * self.y
        dy = alpha * (self.cycle_r ** 2 - r ** 2) * self.y + omega * self.x

        # Euler method to update the state
        self.x += dx * self.dt
        self.y += dy * self.dt

        # decay if needed
        self.x = torch.where(r > self.cycle_r_min, self.x * self.ratio_change, self.x)
        self.y = torch.where(r > self.cycle_r_min, self.y * self.ratio_change, self.y)

        # map the state to the limit cycle
        r = torch.sqrt(self.x ** 2 + self.y ** 2)

        self.x = torch.where(r > self.cycle_r, self.x / r, self.x)
        self.y = torch.where(r > self.cycle_r, self.y / r, self.y)

    # ---------------------------------------------------------------

    def reset(self, env_ids=None, randomize=False):
        """
        reset the state of the oscillator

        step:
        1. set phase
        2. calculate x, y
        3. add phase offset
        4. set x, y
        """
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        if randomize:
            rand_phase = torch.rand(size=env_ids.shape, device=self.device) * 2 * torch.pi
            rand_phase = rand_phase.unsqueeze(1).repeat(1, self.num_feet)

            self.x[env_ids] = torch.cos(rand_phase)
            self.y[env_ids] = torch.sin(rand_phase)
        else:
            non_rand_phase = torch.zeros(env_ids.shape, device=self.device)
            non_rand_phase = non_rand_phase.unsqueeze(1).repeat(1, self.num_feet)

            self.x[env_ids] = torch.cos(non_rand_phase)
            self.y[env_ids] = torch.sin(non_rand_phase)

        self.set_phase_offset(env_ids=env_ids, phase_offset=self.phase_offset[env_ids])

    def step(self):
        self._cpg_hopf_oscillator()

    # ---------------------------------------------------------------

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_rate(self, rate):
        self.rate = rate

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_phase_offset(self, env_ids=None, phase_offset=None):
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        if phase_offset is None:
            phase_offset = torch.zeros((env_ids.shape[0], self.num_feet), device=self.device)
        else:
            phase_offset = phase_offset

        # update phase offset
        self.phase_offset[env_ids] = phase_offset

        # update x, y based on the new phase offset
        phase_now_of_env_ids = self.get_phase_base(env_ids)
        phase_new_of_env_ids = phase_now_of_env_ids + self.get_phase_offset(env_ids)

        self.x[env_ids] = torch.cos(phase_new_of_env_ids)
        self.y[env_ids] = torch.sin(phase_new_of_env_ids)

    def set_ratio_contact(self, ratio_contact):
        self.ratio_contact = ratio_contact

    def set_ratio_change(self, ratio_change):
        self.ratio_change = ratio_change

    # ---------------------------------------------------------------

    def set_stand_pattern(self, env_ids=None):
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        self.ratio_change[env_ids] = self.ratio_change_decrease
        self.ratio_contact[env_ids] = 0.50

    def set_walk_pattern(self, env_ids=None):
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        self.ratio_change[env_ids] = self.ratio_change_increase
        self.ratio_contact[env_ids] = 0.65

    def set_run_pattern(self, env_ids=None):
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        self.ratio_change[env_ids] = self.ratio_change_increase
        self.ratio_contact[env_ids] = 0.40

    # ---------------------------------------------------------------

    def get_x(self, env_ids=None):
        """
        get the x value of the oscillators

        return:
        x: [num_envs, num_feet]
        """
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        return self.x[env_ids]

    def get_y(self, env_ids=None):
        """
        get the y value of the oscillators

        return:
        y: [num_envs, num_feet]
        """
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        return self.y[env_ids]

    def get_phase_base(self, env_ids=None):
        """
        get the base phase of the oscillators, the base phase is the phase of oscillator[0],
        but need to extend to all oscillators shape=[num_envs, num_feet]

        return:
        phase: [num_envs, num_feet], range: [0, 2 * pi]
        """
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        phi = torch.atan2(self.y[env_ids, 0], self.x[env_ids, 0])
        phase = torch.where(phi < 0, phi + 2 * torch.pi, phi)
        phase = phase.unsqueeze(1).repeat(1, self.num_feet)

        return phase

    def get_phase_rad(self, env_ids=None):
        """
        get the phase of the oscillators

        return:
        phase: [num_envs, num_feet], range: [0, 2 * pi]
        """
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        phi = torch.atan2(self.y[env_ids], self.x[env_ids])
        phase = torch.where(phi < 0, phi + 2 * torch.pi, phi)

        return phase

    def get_phase_norm(self, env_ids=None):
        """
        get the normalized phase of the oscillators

        return:
        phase_norm: [num_envs, num_feet], range: [0, 1]
        """
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        phase_norm = self.get_phase_rad(env_ids=env_ids) / (2 * torch.pi)
        return phase_norm

    def get_phase_offset(self, env_ids=None):
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        else:
            env_ids = env_ids

        return self.phase_offset[env_ids]

    def get_foot_height(self, type=FOOT_HEIGHT_TYPE_LINEAR) -> torch.Tensor:
        """
        map the y value to the foot height
        """
        foot_height_raw = torch.where(self.y <= self.cycle_r_min, 0, self.y - self.cycle_r_min)
        foot_height_raw = foot_height_raw / (self.cycle_r - self.cycle_r_min)

        if type == self.FOOT_HEIGHT_TYPE_LINEAR:
            self.foot_height = (foot_height_raw ** 1) * self.foot_height_target
        elif type == self.FOOT_HEIGHT_TYPE_SMOOTH:
            self.foot_height = (foot_height_raw ** 2) * self.foot_height_target
        else:
            self.foot_height = (foot_height_raw ** 1) * self.foot_height_target

        return self.foot_height

    def get_foot_height_norm(self):
        foot_height = self.get_foot_height()
        foot_height_norm = foot_height / self.foot_height_target

        return foot_height_norm

    def get_foot_contact(self) -> torch.Tensor:
        foot_contact_raw = torch.where(self.y <= self.cycle_r_min, 1, 0)
        self.foot_contact = foot_contact_raw
        return self.foot_contact

    def get_swing_middle(self, type=SWING_MIDDLE_TYPE_LINEAR) -> torch.Tensor:
        """
        get the swing middle value

        type:
        - SWING_MIDDLE_TYPE_LINEAR: linear
        - SWING_MIDDLE_TYPE_ACCURATE: accurate

        return:
        swing_middle: [num_envs, num_feet]

        note:
        stand situation will have a swing_middle value of 0
        swing situation will have a swing_middle value of 1
        """
        # only consider the foot height above the middle situation
        foot_height_norm = self.get_foot_height_norm()
        foot_height_norm = torch.where(foot_height_norm > 0.5, foot_height_norm - 0.5, 0)
        foot_height_norm = foot_height_norm * 2

        if type == self.SWING_MIDDLE_TYPE_LINEAR:
            swing_middle = foot_height_norm ** 1
        elif type == self.SWING_MIDDLE_TYPE_ACCURATE:
            swing_middle = foot_height_norm ** 3
        else:
            swing_middle = foot_height_norm ** 1

        return swing_middle


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    time = range(50)
    value_list = []

    gait_generator = FourierGaitGenerator(
        num_envs=1,
        num_feet=2,
        dt=0.02,  # 50Hz
        phase_offset=torch.tensor([0.0, torch.pi]),
        device="cpu")

    gait_generator.reset(env_ids=torch.tensor([0]), randomize=True)

    for i in time:
        gait_generator.step()
        value = gait_generator.get_swing_middle(type=FourierGaitGenerator.SWING_MIDDLE_TYPE_ACCURATE)
        value_list.append(value.numpy()[0])

    plt.plot(time, value_list)
    plt.show()

    # time = range(1000)
    # source_signal = torch.sin(torch.tensor([0.01 * i for i in time]))
    # target_signal = torch.sin(torch.tensor([0.01 * i for i in time]))
    #
    # source_signal = torch.where(source_signal < 0, 0, source_signal)
    # target_signal = source_signal ** 2
    #
    # # plot
    # plt.plot(time, source_signal, label="source")
    # plt.plot(time, target_signal, label="target")
    # plt.legend()
    # plt.show()
