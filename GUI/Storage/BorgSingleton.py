class BorgSingleton:
    """
    Singleton Class to store shared data in Application Runtime
    """
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class ExperimentSingleton(BorgSingleton):
    """
    Singleton Class to store Experiment Data in Application Runtime
    """

    def __init__(self, firstname=None, lastname=None, experiment_id=None, plasmids=None, plasmid_tubes=None, date=None):
        BorgSingleton.__init__(self)
        if firstname is not None:
            self.firstname = firstname
        if lastname is not None:
            self.lastname = lastname
        if experiment_id is not None:
            self.experiment_id = experiment_id
        if plasmids is not None:
            self.plasmids = plasmids
        if plasmid_tubes is not None:
            self.plasmid_tubes = plasmid_tubes
        if date is not None:
            self.date = date

    def __str__(self):
        return f'ExperimentSingleton(firstname={self.firstname}, lastname={self.lastname}, experimentId={self.experiment_id}, plasmids={self.plasmids}, tubes={self.plasmid_tubes}, date={self.date})'


class TubesSingleton(BorgSingleton):
    """
        Singleton Class to store Tubes Data in Application Runtime
    """

    def __init__(self):
        BorgSingleton.__init__(self)

        if not hasattr(self, 'tubes'):
            self.tubes = {}

    def add_tube(self, tube, qr_code, plasmid_nr):
        self.tubes[tube] = {'qr_code': qr_code, 'plasmid_nr': plasmid_nr}

    def __str__(self):
        return f'TubesSingleton(tubes={self.tubes})'


if __name__ == "__main__":
    # Use cases test, could be ignored
    borg = BorgSingleton()
    exp1 = ExperimentSingleton("Ujwal", "Subedi", "ujwal1", ['PHB30', 'PHB40'], {'PHB30': '4,5,6', 'PHB40': '1,2,3'},
                               '03.12.2023')
    print(exp1)
    exp2 = ExperimentSingleton("Wissam", "Alamareen", "wissam1", ['PHB35', 'PHB45'],
                               {'PHB35': '4,5,6', 'PHB45': '1,2,3'},
                               '03.12.2023')
    print(exp2)
    tubes1 = TubesSingleton()
    tubes1.add_tube('tube1', 'qr123', 'plasmid456')
    print(tubes1)

    tubes2 = TubesSingleton()
    print(tubes2)
    print(borg.__dict__.items())

    exp3 = ExperimentSingleton()
    print(exp3)
