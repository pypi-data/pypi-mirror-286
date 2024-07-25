class Pit:
    def __init__(self, name, leak_detector_id=None, leak_detector_pmid=None,
                 leak_detector_tfsps=None, tfsps_transmitter=None, tfsps_pmid=None,
                 drain_seal_location=None, drain_seal_name = None, drain_seal_position=None,
                 annulus_leak_detector=None, annulus_leak_detector_pmid=None,
                 pit_nace=None, pit_nace_pmid=None, in_pit_heater=None,
                 tfmcs=None, tsr_structure=None):
        self.components = []
        self.name = name
        self.leak_detector_id = leak_detector_id
        self.leak_detector_pmid = leak_detector_pmid
        self.leak_detector_tfsps = leak_detector_tfsps
        self.tfsps_transmitters = [tfsps_transmitter] if tfsps_transmitter else []
        self.tfsps_pmids = [tfsps_pmid] if tfsps_pmid else []
        self.drain_seal_location = drain_seal_location
        self.drain_seal_name = drain_seal_name
        self.drain_seal_position = drain_seal_position
        self.annulus_leak_detectors = [annulus_leak_detector] if annulus_leak_detector else []
        self.annulus_leak_detector_pmids = [annulus_leak_detector_pmid] if annulus_leak_detector_pmid else []
        self.pit_nace = pit_nace
        self.pit_nace_pmid = pit_nace_pmid
        self.in_pit_heaters = [in_pit_heater] if in_pit_heater else []
        self.tfmcs = tfmcs
        self.tsr_structure = tsr_structure

    def add_used_component(self, node):
            self.components.append(node)

    def update(self, **kwargs):
            self.tfsps_transmitters.append(kwargs['tfsps_transmitter'])
            self.tfsps_pmids.append(kwargs['tfsps_pmid'])
            self.annulus_leak_detectors.append(kwargs['annulus_leak_detector'])
            self.annulus_leak_detector_pmids.append(kwargs['annulus_leak_detector_pmid'])
            if kwargs['in_pit_heater'] is not None:
                   self.in_pit_heaters.append(kwargs['in_pit_heater']) 

