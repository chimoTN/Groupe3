import dataclasses

@dataclasses.dataclass
class caution():
    nameClient: str
    nameEmployer: str
    dateSigniature: str
    signatureClient: str
    signatureEmployer: str

    #On signe la cotion
    def signiatureCautionClient():
        pass 

    #On signe la cotion
    def signiatureCautionEmployer():
        pass 

