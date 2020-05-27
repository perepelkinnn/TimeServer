import struct


class Packet:
    _FORMAT = "!4b11I"

    def __init__(self, version_number=2, mode=3, reference=0, originate=0, receive=0, transmit=0):
        self.leap_indicator = 0
        self.version_number = version_number
        self.mode = mode
        self.stratum = 0
        self.pool = 0
        self.precision = 0
        self.root_delay = 0
        self.root_dispersion = 0
        self.ref_id = 0
        self.reference = reference
        self.originate = originate
        self.receive = receive
        self.transmit = transmit

    def pack(self):
        return struct.pack(Packet._FORMAT,
                           (self.leap_indicator << 6) +
                           (self.version_number << 3) + self.mode,
                           self.stratum,
                           self.pool,
                           self.precision,
                           int(self.root_delay) +
                           get_fraction(self.root_delay, 16),
                           int(self.root_dispersion) +
                           get_fraction(self.root_dispersion, 16),
                           ascii_to_int(self.ref_id),
                           int(self.reference),
                           get_fraction(self.reference, 32),
                           int(self.originate),
                           get_fraction(self.originate, 32),
                           int(self.receive),
                           get_fraction(self.receive, 32),
                           int(self.transmit),
                           get_fraction(self.transmit, 32))

    def unpack(self, data: bytes):
        unpacked_data = struct.unpack(Packet._FORMAT, data)

        self.leap_indicator = unpacked_data[0] >> 6
        self.version_number = unpacked_data[0] >> 3 & 0b111
        self.mode = unpacked_data[0] & 0b111

        self.stratum = unpacked_data[1]
        self.pool = unpacked_data[2]
        self.precision = unpacked_data[3]

        self.root_delay = (unpacked_data[4] >> 16) + \
            (unpacked_data[4] & 0xFFFF) / 2 ** 16
        self.root_dispersion = (unpacked_data[5] >> 16) + \
            (unpacked_data[5] & 0xFFFF) / 2 ** 16

        self.ref_id = chr((unpacked_data[6] >> 24) & 0xFF) + \
            chr((unpacked_data[6] >> 16) & 0xFF) +  \
            chr((unpacked_data[6] >> 8) & 0xFF) +  \
            chr(unpacked_data[6] & 0xFF)

        self.reference = unpacked_data[7] + unpacked_data[8] / 2 ** 32
        self.originate = unpacked_data[9] + unpacked_data[10] / 2 ** 32
        self.receive = unpacked_data[11] + unpacked_data[12] / 2 ** 32
        self.transmit = unpacked_data[13] + unpacked_data[14] / 2 ** 32

        return self

    def to_display(self):
        return "Leap indicator: {0.leap_indicator}\n" \
            "Version number: {0.version_number}\n" \
            "Mode: {0.mode}\n" \
            "Stratum: {0.stratum}\n" \
            "Pool: {0.pool}\n" \
            "Precision: {0.precision}\n" \
            "Root delay: {0.root_delay}\n" \
            "Root dispersion: {0.root_dispersion}\n" \
            "Ref id: {0.ref_id}\n" \
            "Reference: {0.reference}\n" \
            "Originate: {0.originate}\n" \
            "Receive: {0.receive}\n" \
            "Transmit: {0.transmit}"\
            .format(self)


def get_fraction(number, precision):
    return int((number - int(number)) * 2 ** precision)


def ascii_to_int(s):
    try:
        c = list(map(ord, s))
        return int(c[0] << 24) + int(c[1] << 16) + int(c[2] << 8) + int(c[3])
    except TypeError:
        pass
    return 0
