#!/usr/bin/env python3

import device

dev = device.SpectrumAnalyzer()

dev.set_center_frequency(0.03)
dev.set_span(0.04)

dev.sweep()
dev.get_trace()
