from fourier_core.end_effector.fi_end_effector_base import EndEffectorBase


class EndEffectorGR1(EndEffectorBase):
    def __init__(self, joints=None):
        super().__init__(joints)

    def forward_kinematics(self):
        pass

    def inverse_kinematics(self):
        pass

    def forward_dynamics(self):
        pass

    def inverse_dynamics(self):
        pass
