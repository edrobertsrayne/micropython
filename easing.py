import math


class EasingFunction:
    @staticmethod
    def linear(progress):
        return progress

    @staticmethod
    def quadratic_in(progress):
        return progress * progress

    @staticmethod
    def quadratic_out(progress):
        return progress * (2 - progress)

    @staticmethod
    def quadratic_inout(progress):
        if progress < 0.5:
            return 2 * progress * progress
        else:
            return -1 + (4 - 2 * progress) * progress

    @staticmethod
    def cubic_in(progress):
        return progress * progress * progress

    @staticmethod
    def cubic_out(progress):
        return 1 + (progress - 1) * (progress - 1) * (progress - 1)

    @staticmethod
    def cubic_inout(progress):
        if progress < 0.5:
            return 4 * progress * progress * progress
        else:
            return 1 + (progress - 1) * (2 - (progress - 1) * (progress - 1))

    @staticmethod
    def quartic_in(progress):
        return progress * progress * progress * progress

    @staticmethod
    def quartic_out(progress):
        return 1 - (progress - 1) * (progress - 1) * (progress - 1) * (progress - 1)

    @staticmethod
    def quartic_inout(progress):
        if progress < 0.5:
            return 8 * progress * progress * progress * progress
        else:
            return 1 - 8 * (progress - 1) * (progress - 1) * (progress - 1) * (
                progress - 1
            )

    @staticmethod
    def quintic_in(progress):
        return progress * progress * progress * progress * progress

    @staticmethod
    def quintic_out(progress):
        return 1 + (progress - 1) * (progress - 1) * (progress - 1) * (progress - 1) * (
            progress - 1
        )

    @staticmethod
    def quintic_inout(progress):
        if progress < 0.5:
            return 16 * progress * progress * progress * progress * progress
        else:
            return 1 + 16 * (progress - 1) * (progress - 1) * (progress - 1) * (
                progress - 1
            ) * (progress - 1)

    @staticmethod
    def sinusoidal_in(progress):
        return math.sin((progress - 1) * math.pi / 2) + 1

    @staticmethod
    def sinusoidal_out(progress):
        return math.sin(progress * math.pi / 2)

    @staticmethod
    def sinusoidal_inout(progress):
        return (1 + math.sin(math.pi * (progress - 0.5))) / 2

    @staticmethod
    def exponential_in(progress):
        if progress == 0:
            return 0
        return math.pow(2, 10 * (progress - 1))

    @staticmethod
    def exponential_out(progress):
        if progress == 1:
            return 1
        return 1 - math.pow(2, -10 * progress)

    @staticmethod
    def exponential_inout(progress):
        if progress == 0:
            return 0
        if progress == 1:
            return 1
        if progress < 0.5:
            return 0.5 * math.pow(2, (20 * progress) - 10)
        else:
            return -0.5 * math.pow(2, (-20 * progress) + 10) + 1

    @staticmethod
    def circular_in(progress):
        return 1 - math.sqrt(1 - progress * progress)

    @staticmethod
    def circular_out(progress):
        return math.sqrt((2 - progress) * progress)

    @staticmethod
    def circular_inout(progress):
        if progress < 0.5:
            return (1 - math.sqrt(1 - 4 * (progress * progress))) / 2
        else:
            return (math.sqrt(-(2 * progress - 3) * (2 * progress - 1)) + 1) / 2

    @staticmethod
    def elastic_in(progress):
        if progress == 0:
            return 0
        if progress == 1:
            return 1
        return -(2 ** (10 * (progress - 1))) * math.sin(
            (progress - 1.075) * (2 * math.pi) / 0.3
        )

    @staticmethod
    def elastic_out(progress):
        if progress == 0:
            return 0
        if progress == 1:
            return 1
        return (2 ** (-10 * progress)) * math.sin(
            (progress - 0.075) * (2 * math.pi) / 0.3
        ) + 1

    @staticmethod
    def elastic_inout(progress):
        if progress == 0:
            return 0
        if progress == 1:
            return 1
        if progress < 0.5:
            return (
                -(2 ** (20 * progress - 10))
                * math.sin((20 * progress - 11.125) * math.pi / 4.5)
                / 2
            )
        else:
            return (2 ** (-20 * progress + 10)) * math.sin(
                (20 * progress - 11.125) * math.pi / 4.5
            ) / 2 + 1

    @staticmethod
    def back_in(progress):
        return progress * progress * ((1.70158 + 1) * progress - 1.70158)

    @staticmethod
    def back_out(progress):
        return (progress - 1) * (progress - 1) * (
            (1.70158 + 1) * (progress - 1) + 1.70158
        ) + 1

    @staticmethod
    def back_inout(progress):
        if progress < 0.5:
            return (
                (2 * progress)
                * (2 * progress)
                * ((2.5949 + 1) * (2 * progress) - 2.5949)
                / 2
            )
        else:
            return (2 * progress - 2) * (2 * (progress - 1)) * (
                (2.5949 + 1) * (2 * (progress - 1)) + 2.5949
            ) / 2 + 1

    @staticmethod
    def bounce_in(progress):
        return 1 - EasingFunction.bounce_out(1 - progress)

    @staticmethod
    def bounce_out(progress):
        if progress < 1 / 2.75:
            return 7.5625 * progress * progress
        elif progress < 2 / 2.75:
            return 7.5625 * (progress - 1.5 / 2.75) * (progress - 1.5 / 2.75) + 0.75
        elif progress < 2.5 / 2.75:
            return 7.5625 * (progress - 2.25 / 2.75) * (progress - 2.25 / 2.75) + 0.9375
        else:
            return (
                7.5625 * (progress - 2.625 / 2.75) * (progress - 2.625 / 2.75)
                + 0.984375
            )

    @staticmethod
    def bounce_inout(progress):
        if progress < 0.5:
            return (1 - EasingFunction.bounce_out(1 - 2 * progress)) / 2
        else:
            return (1 + EasingFunction.bounce_out(2 * progress - 1)) / 2
