With FDSolver
.Reset 
.SetMethod "Tetrahedral", "General Purpose"
.OrderTet "Second"
.Type "Direct"
.Stimulation "List", "List"
.ResetExcitationList 
.AddToExcitationList "Zmax", "TE(0,0)"
.AccuracyTet "1e-5"
.MeshAdaptionTet "False"
.FrequencySamples "220"
.SetNumberOfResultDataSamples "2951"
.SetResultDataSamplingMode "Frequency (linear)"
.UseParallelization "True"
.MaxCPUs "8"
.SetStopSweepIfCriterionMet "True"
.SetSweepThreshold "S-Parameters", "0.01"
.SweepErrorChecks "3"
.SweepMinimumSamples "15"
End With
With MeshAdaption3D
.SetType "HighFrequencyTet"
.MinPasses "2"
.MaxPasses "3"
.MaxDeltaS "0.02"
.NumberOfDeltaSChecks "1"
.RemoveAllUserDefinedStopCriteria 
.AddStopCriterion "All S-Parameters", "0.02", "1", "True"
End With