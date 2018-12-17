import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
                                     args = cms.vstring('/afs/cern.ch/user/p/pbryant/public/ggHZ_HanythingJ_NNPDF31_13TeV_M125_Vleptonic/v1/ggHZ_HanythingJ_NNPDF31_13TeV_M125_Vhadronic_filterB.tgz'),
                                     nEvents = cms.untracked.uint32(5000),
                                     numberOfParameters = cms.uint32(1),
                                     outputFile = cms.string('cmsgrid_final.lhe'),
                                     scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
                                     )

lheGenericFilter = cms.EDFilter("LHEGenericFilter",
                                src = cms.InputTag("externalLHEProducer"),
                                NumRequired = cms.int32(1),
                                ParticleID = cms.vint32(5),
                                AcceptLogic = cms.string("GT"),     # LT meaning < NumRequired, GT >, EQ =, NE !=
                                )

#link for cards
#https://github.com/patrickbryant/genproductions/blob/master/bin/Powheg/production/2017/13TeV/Higgs/ggHZ_HanythingJ_NNPDF31_13TeV/ggHZ_HanythingJ_NNPDF31_13TeV_M125_Vhadronic.input

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                                     pythia8CP5SettingsBlock,
                                                     pythia8PSweightsSettingsBlock,
                                                     pythia8PowhegEmissionVetoSettingsBlock,
                                                     processParameters = cms.vstring('POWHEG:nFinal = 2',   ## Number of final state particles
                                                                                     ## (BEFORE THE DECAYS) in the LHE
                                                                                     ## other than emitted extra parton
                                                                                     '25:m0 = 125.0',
                                                                                     '25:onMode = off',
                                                                                     '25:onIfMatch = 5 -5',
                                                                                     ),
                                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                                 'pythia8CP5Settings',
                                                                                 'pythia8PowhegEmissionVetoSettings',
                                                                                 'pythia8PSweightsSettings',
                                                                                 'processParameters'
                                                                                 )
                                                     )
                         )

ProductionFilterSequence = cms.Sequence(generator)
